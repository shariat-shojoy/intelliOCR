from pathlib import Path
import pytesseract
import re
from PIL import Image
from tqdm import tqdm

# ============================================================
# CONFIG
# ============================================================

IMAGE_FOLDER = Path("split_pages")
OUTPUT_FILE = "bangla_academi_words.txt"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

OCR_CONFIG = r"--oem 1 --psm 6"

# ============================================================
# CLEANING REGEX
# ============================================================

REMOVE_PATTERNS = [

    r"\[[^\]]*\]",      # [বি]
    r"\([^)]*\)",       # (...)
    r"\{[^}]*\}",

    r"\+.*",            # +তা
    r",.*",
    r";.*",
    r":.*",

    r"'[^']*'",
    r'"[^"]*"',

    r"[0-9০-৯]+",

]

compiled = [re.compile(x) for x in REMOVE_PATTERNS]

BANGLA_RE = re.compile(r"^[\u0980-\u09FF]+$")


def clean(word):

    word = word.strip()

    for p in compiled:
        word = p.sub("", word)

    # Keep Bangla Unicode only
    word = "".join(c for c in word if '\u0980' <= c <= '\u09FF')

    word = word.strip("।,;:[](){}-— ")

    if len(word) < 2:
        return None

    if not BANGLA_RE.fullmatch(word):
        return None

    return word


# ============================================================
# OCR
# ============================================================

all_words = set()

images = sorted(IMAGE_FOLDER.glob("*.png"))

for img_path in tqdm(images):

    image = Image.open(img_path)

    text = pytesseract.image_to_string(
        image,
        lang="ben",
        config=OCR_CONFIG
    )

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        first = line.split()[0]

        word = clean(first)

        if word:
            all_words.add(word)

# ============================================================
# SORT
# ============================================================

words = sorted(all_words)

# ============================================================
# SAVE
# ============================================================

with open(OUTPUT_FILE, "w", encoding="utf8") as f:

    for w in words:

        f.write(w + "\n")

print("="*40)
print("Finished")
print("Unique words:", len(words))
print("="*40)