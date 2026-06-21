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


def encode(image_path, message, output_path):
    """Hide a secret message inside an image using LSB"""
    img = Image.open(image_path)

    # Convert the message to bits and add the end marker
    binary_message = text_to_binary(message) + DELIMITER

    # Load pixel data so we can edit it
    pixels = img.load()
    width, height = img.size

    index = 0  # tracks which bit we hiding next

    for y in range(height):
        for x in range(width):
            # Get the RGB values of this pixel
            r, g, b = img.getpixel((x, y))[:3]

            # Replace the LSB of each color channel with a message bit
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

            # Stop once the whole message is hidden
            if index >= len(binary_message):
                img.save(output_path)
                print(f"message hidden: saved to {output_path}")
                return

    print("image too small to hold this message")
    
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
    img = Image.open(image_path)
    width, height = img.size

    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))[:3]

            # Read the LSB of each color channel
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

            # Check if we've reached the end marker
            if DELIMITER in binary_data:
                # Cut off everything from the delimiter onward
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