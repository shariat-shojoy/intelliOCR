from pathlib import Path
import fitz

# =====================================================
# CONFIG
# =====================================================

PDF_FILE = Path("WB_BANGLA_ACADEMY_WORD_LIST.pdf")

OUTPUT_DIR = Path("split_pages")

DPI = 600

# Pixel ranges (X coordinates)
COLUMNS = [
    (0, 1390),
    (1390, 2640),
    (2640, 3840),
    (3840, 5070),
]

# =====================================================

OUTPUT_DIR.mkdir(exist_ok=True)

doc = fitz.open(PDF_FILE)

print(f"Total Pages : {len(doc)}")

for page_no in range(len(doc)):

    page = doc.load_page(page_no)

    # Render once to determine the page size in pixels.
    pix = page.get_pixmap(dpi=DPI)

    page_width_px = pix.width
    page_height_px = pix.height

    # Convert pixel-based crop ranges to PDF point coordinates.
    scale_x = page.rect.width / page_width_px
    scale_y = page.rect.height / page_height_px

    print(f"Processing Page {page_no+1}/{len(doc)}")

    for col_no, (x1, x2) in enumerate(COLUMNS, start=1):

        # Prevent overflow and keep the crop valid.
        x1 = max(0, x1)
        x2 = min(page_width_px, x2)

        if x2 <= x1:
            continue

        clip = fitz.Rect(
            x1 * scale_x,
            0,
            x2 * scale_x,
            page.rect.height
        )

        cropped = page.get_pixmap(
            dpi=DPI,
            clip=clip
        )

        save_path = OUTPUT_DIR / f"page_{page_no+1:04d}_col{col_no}.png"

        cropped.save(save_path)

doc.close()

print("\nDone!")
print(f"Images saved in: {OUTPUT_DIR.resolve()}")