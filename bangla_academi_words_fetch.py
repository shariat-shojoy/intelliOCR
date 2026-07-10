from pathlib import Path
import fitz
import pytesseract
import cv2
import numpy as np
import re

from PIL import Image
from tqdm import tqdm

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PDF_FILE = BASE_DIR / "WB_BANGLA_ACADEMY_WORD_LIST.pdf"
OUTPUT_FILE = BASE_DIR / "bangla_academi_words.txt"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if Path(TESSERACT_PATH).exists():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

DPI = 800

# -------------------------------------------------------
# CLEANING
# -------------------------------------------------------

REMOVE_PATTERNS = [

    r"\[[^\]]*\]",      # [বি]
    r"\([^)]*\)",       # (...)
    r"\+.*",            # +তা
    r",.*",             # , ....
    r"'[^']*'",         # 'Akademi'
]

compiled = [re.compile(x) for x in REMOVE_PATTERNS]
def detect_columns(gray):
    """
    Automatically detect text columns using vertical projection.
    Returns list of cropped column images.
    """

    # Binary image (text = white)
    _, binary = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Vertical projection
    projection = np.sum(binary > 0, axis=0)

    threshold = projection.max() * 0.08

    inside = False
    start = 0
    regions = []

    for i, v in enumerate(projection):

        if not inside and v > threshold:
            inside = True
            start = i

        elif inside and v <= threshold:
            inside = False
            if i - start > 80:
                regions.append((start, i))

    if inside:
        regions.append((start, len(projection)-1))

    # Merge close regions
    merged = []

    for r in regions:

        if not merged:
            merged.append(list(r))
        else:

            if r[0] - merged[-1][1] < 40:
                merged[-1][1] = r[1]
            else:
                merged.append(list(r))

    columns = []

    for x1, x2 in merged:

        pad = 15

        x1 = max(0, x1-pad)
        x2 = min(gray.shape[1], x2+pad)

        columns.append(gray[:, x1:x2])

    return columns

def clean(word):

    for p in compiled:
        word = p.sub("", word)

    # keep Bangla only
    word = "".join(c for c in word if '\u0980' <= c <= '\u09FF')

    word = word.strip()

    if len(word) < 2:
        return None

    return word


# -------------------------------------------------------
# OCR ONE PAGE
# -------------------------------------------------------

def process_page(doc, page_number):

    page = doc.load_page(page_number)

    pix = page.get_pixmap(dpi=DPI)

    img = np.frombuffer(pix.samples, dtype=np.uint8)

    img = img.reshape(pix.height, pix.width, pix.n)

    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Threshold

    gray = cv2.fastNlMeansDenoising(gray)

    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    columns = detect_columns(gray)

    text = ""

    for col in columns:

        txt = pytesseract.image_to_string(
            Image.fromarray(col),
            lang="ben",
            config="--oem 1 --psm 4 -c preserve_interword_spaces=1"
        )

        text += txt + "\n"

    words = set()

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        first = line.split()[0]

        first = clean(first)

        if first:
            words.add(first)

    return words


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

def main():
    if not PDF_FILE.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_FILE}")

    doc = fitz.open(str(PDF_FILE))
    total_pages = len(doc)

    all_words = set()

    for page_number in tqdm(range(total_pages), total=total_pages):
        all_words.update(process_page(doc, page_number))

    doc.close()

    # Unicode sort
    words = sorted(all_words)

    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        for w in words:
            f.write(w + "\n")

    print("Done")
    print("Total unique words:", len(words))


if __name__ == "__main__":
    main()