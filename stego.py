import os
import argparse
from PIL import Image

def text_to_binary(text):
    """Convert text into a string of bits"""
    binary = ""
    for char in text:
        # ord() gives the ASCII number, then format it as 8-bit binary
        binary += format(ord(char), '08b')
    return binary

# This marker tells the decoder where the hidden message ends
DELIMITER = "1111111111111110"

def get_capacity(img):
    """Return how many characters an image can hold."""
    width, height = img.size
    # 3 bits per pixel (R, G, B), 8 bits per character
    total_bits = width * height * 3
    # Subtract the delimiter length, then convert bits to characters
    return (total_bits - len(DELIMITER)) // 8

def encode(image_path, message, output_path):
    """Hide a secret message inside an image using LSB"""
    # Check the file exists first
    if not os.path.exists(image_path):
        print(f"Error: file '{image_path}' not found")
        return

    try:
        img = Image.open(image_path)
    except Exception:
        print(f"Error: '{image_path}' is not a valid image")
        return

    # Convert to RGB so we always have 3 channels to work with
    img = img.convert("RGB")

    # Make sure the message actually fits
    capacity = get_capacity(img)
    if len(message) > capacity:
        print(f"Error: message too long. this image holds up to {capacity} characters, "
              f"but your message has {len(message)}.")
        return

    binary_message = text_to_binary(message) + DELIMITER
    pixels = img.load()
    width, height = img.size
    index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            if index < len(binary_message):
                r = (r & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                g = (g & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                b = (b & ~1) | int(binary_message[index])
                index += 1

            pixels[x, y] = (r, g, b)

            if index >= len(binary_message):
                img.save(output_path)
                print(f"message hidden: saved to {output_path}")
                return
    
def binary_to_text(binary):
    """Convert a string of bits back into text"""
    text = ""
    # Process 8 bits at a time (one character)
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        text += chr(int(byte, 2))
    return text

def decode(image_path):
    """Extract a hidden message from an image"""
    if not os.path.exists(image_path):
        print(f"Error: file '{image_path}' not found")
        return None

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception:
        print(f"Error: '{image_path}' is not a valid image")
        return None

    width, height = img.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

            if DELIMITER in binary_data:
                binary_data = binary_data[:binary_data.index(DELIMITER)]
                message = binary_to_text(binary_data)
                print(f"Hidden message: {message}")
                return message

    print("no hidden message found")
    return None

def main():
    # Set up the main parser
    parser = argparse.ArgumentParser(
        description="Hide and reveal secret messages inside images (LSB steganography)"
    )

    # we use subcommands: "encode" and "decode"
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- encode command ---
    encode_parser = subparsers.add_parser("encode", help="Hide a message in an image")
    encode_parser.add_argument("-i", "--image", required=True, help="Path to the input image")
    encode_parser.add_argument("-m", "--message", required=True, help="The secret message to hide")
    encode_parser.add_argument("-o", "--output", required=True, help="Path to save the output image")

    # --- decode command ---
    decode_parser = subparsers.add_parser("decode", help="Reveal a hidden message")
    decode_parser.add_argument("-i", "--image", required=True, help="Path to the image to read")

    # Read what the user typed
    args = parser.parse_args()

    # Run the matching function
    if args.command == "encode":
        encode(args.image, args.message, args.output)
    elif args.command == "decode":
        decode(args.image)


# This runs main() only when the file is executed directly
if __name__ == "__main__":
    main()