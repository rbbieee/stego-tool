def xor_cipher(text, key):
    """Encrypt or decrypt text using XOR with a key.

    Because XOR is its own inverse, the same function
    handles both encryption and decryption.
    """
    result = ""
    for i, char in enumerate(text):
        # Cycle through the key if it's shorter than the text
        key_char = key[i % len(key)]
        # XOR the character codes, then turn back into a character
        result += chr(ord(char) ^ ord(key_char))
    return result