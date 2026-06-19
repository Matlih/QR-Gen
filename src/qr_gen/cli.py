import argparse
import sys
from pathlib import Path

from qr_gen.core import generate_qr

def main():
    parser = argparse.ArgumentParser(
        description="Generate a modern QR code with optional logo and custom colors."
    )
    parser.add_argument("data", help="URL or text to encode in the QR code")
    parser.add_argument(
        "-o", "--output", default="qrcode.png", help="Output file path (default: qrcode.png)"
    )
    parser.add_argument(
        "-fc", "--fill-color", default="black", help="Color of the QR code (default: black)"
    )
    parser.add_argument(
        "-bc", "--back-color", default="white", help="Background color (default: white)"
    )
    parser.add_argument(
        "-l", "--logo", default=None, help="Path to a logo image to center in the QR code"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=10, help="Box size for the QR grid (default: 10)"
    )

    args = parser.parse_args()

    try:
        saved_path = generate_qr(
            url_or_text=args.data,
            output_path=args.output,
            box_size=args.size,
            fill_color=args.fill_color,
            back_color=args.back_color,
            logo_path=args.logo,
        )
        print(f"Success! QR code saved to: {saved_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
