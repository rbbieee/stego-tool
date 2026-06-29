# Steganography Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pillow](https://img.shields.io/badge/Pillow-10.4.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A simple command line tool to hide and reveal secret messages inside images using least significant bit (LSB) steganography

## Features

- Hide any text message inside a PNG image
- Reveal hidden messages from an encoded image
- Optional password protection using XOR encryption
- Simple graphical interface (GUI) and command line interface (CLI)
- Capacity check so your message always fits
- Clear error messages instead of crashes
- Works fully offline, no data leaves your machine

## Installation

Clone the repository and set up a virtual environment.

```bash
git clone https://github.com/rbbieee/stego-tool.git
cd stego-tool

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Hide a message inside an image:

```bash
python stego.py encode -i input.png -m "your secret message" -o output.png
```

Reveal a hidden message:

```bash
python stego.py decode -i output.png
```

See all available options:

```bash
python stego.py --help
```

## GUI

Prefer a graphical interface? Run the GUI version:

```bash
python gui.py
```

Choose an image, type your message, set an optional password, then click Encode or Decode

## Encryption

You can protect your message with a password. The message is XOR encrypted before being hidden, so even if someone extracts it, they only see scrambled text without the correct password

```bash
python stego.py encode -i input.png -m "secret" -o output.png -p mypassword
python stego.py decode -i output.png -p mypassword
```

Note: XOR is used here for learning purposes. It is not secure enough for protecting truly sensitive data

## Capacity

Each pixel can store 3 bits, one in the least significant bit of each color channel. The rough number of characters an image can hold is: 

capacity = (width * height * 3) / 8

For example, a 132 by 116 image can store around 5740 characters. If your message is too long, the tool will tell you the limit before encoding

## Notes

This tool is built for learning and experimentation. It uses PNG images because they are lossless, so the hidden bits stay intact. Avoid using formats like JPEG, which compress the image and would destroy the hidden data

## License

This project is licensed under the MIT License