# Steganography Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pillow](https://img.shields.io/badge/Pillow-10.4.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A simple command line tool to hide and reveal secret messages inside images using least significant bit (LSB) steganography

## Features

- Hide any text message inside a PNG image
- Reveal hidden messages from an encoded image
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

Choose an image, type your message, and click Encode or Decode

## Capacity

Each pixel can store 3 bits, one in the least significant bit of each color channel. The rough number of characters an image can hold is: 

capacity = (width * height * 3) / 8

For example, a 132 by 116 image can store around 5740 characters. If your message is too long, the tool will tell you the limit before encoding

## Notes

This tool is built for learning and experimentation. It uses PNG images because they are lossless, so the hidden bits stay intact. Avoid using formats like JPEG, which compress the image and would destroy the hidden data

## License

This project is licensed under the MIT License