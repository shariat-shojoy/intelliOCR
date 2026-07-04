from pdf2image import convert_from_path
import os

# ====== Configuration ======
pdf_path = "E:\ocr\jonota-1-99.pdf"          # Path to your PDF
output_dir = "images"                    # Folder to save images
dpi = 300                                # 300 DPI is recommended for OCR
image_format = "png"                     # png or jpg

# ===========================

os.makedirs(output_dir, exist_ok=True)

# Convert PDF pages to images
pages = convert_from_path(pdf_path, dpi=dpi)

for i, page in enumerate(pages, start=1):
    filename = os.path.join(output_dir, f"page_{i:03d}.{image_format}")
    page.save(filename, image_format.upper())
    print(f"Saved: {filename}")

print(f"\nDone! Converted {len(pages)} pages.")