"""
OCR Service
-----------
Extracts text from product images using pytesseract.
Run standalone: python ocr_service.py
"""

import pytesseract
from PIL import Image
import re


def extract_text(image_path: str) -> str:
    """
    Extract raw text from an image using Tesseract OCR.

    Args:
        image_path: Path to the image file (JPEG, PNG, etc.)

    Returns:
        Raw OCR text as a string.
    """
    image = Image.open(image_path)

    # Use LSTM OCR engine with automatic page segmentation
    config = "--oem 3 --psm 6"
    raw_text = pytesseract.image_to_string(image, config=config)

    return raw_text.strip()


def parse_inventory(ocr_text: str) -> list[dict]:
    """
    Convert raw OCR text into structured inventory JSON.
    Handles simple OCR noise (extra spaces, mixed case, etc.)

    Expected input format (one item per line):
        Milk 20
        Bread 10
        Eggs 30

    Returns:
        List of dicts: [{"product_name": str, "quantity": int}, ...]
    """
    inventory = []
    lines = ocr_text.strip().splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match: last token is the quantity (number), rest is product name
        match = re.match(r"^(.*?)\s+(\d+)\s*$", line)
        if match:
            product_name = match.group(1).strip().title()  # normalize casing
            quantity = int(match.group(2))
            inventory.append({"product_name": product_name, "quantity": quantity})
        else:
            # Line doesn't match expected format — skip with a warning
            print(f"[ocr_service] Skipping unrecognized line: '{line}'")

    return inventory


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        # Demo with synthetic text when no image is provided
        print("Usage: python ocr_service.py <image_path>")
        print("\n--- Demo mode (no image) ---")
        demo_text = "Milk 20\nBread 10\nEggs 30"
        print("Raw text:\n", demo_text)
        print("\nParsed inventory:")
        for item in parse_inventory(demo_text):
            print(" ", item)
    else:
        path = sys.argv[1]
        print(f"Extracting text from: {path}")
        text = extract_text(path)
        print("Raw OCR text:\n", text)
        print("\nParsed inventory:")
        for item in parse_inventory(text):
            print(" ", item)
