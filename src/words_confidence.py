import os
import string
import pandas as pd
from PIL import Image
import pytesseract
from tqdm import tqdm

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

IMAGES_DIR = "../images_preprocessed_denoised"
OUTPUT_CSV = "ocr_confidence.csv"

# ----------------------------------------------------
# OCR
# ----------------------------------------------------

def get_words_with_confidence(image_path):
    img = Image.open(image_path)

    data = pytesseract.image_to_data(
        img,
        lang="ben",
        output_type=pytesseract.Output.DICT
    )

    words = []

    for i in range(len(data["text"])):

        text = data["text"][i].strip()

        if text == "":
            continue

        try:
            conf = float(data["conf"][i])
        except:
            conf = -1

        words.append((text, conf))

    return words


# ----------------------------------------------------
# CLEAN
# ----------------------------------------------------

def clean_word(word):
    return word.strip(string.punctuation + "।,;:!?\"'()[]/%")


# ----------------------------------------------------
# MAIN
# ----------------------------------------------------

rows = []

images = sorted(os.listdir(IMAGES_DIR))

for fname in tqdm(images):

    image_path = os.path.join(IMAGES_DIR, fname)

    words = get_words_with_confidence(image_path)

    for word, conf in words:

        word = clean_word(word)

        if word == "":
            continue

        rows.append({
            "image": fname,
            "word": word,
            "confidence": conf
        })

# ----------------------------------------------------
# SAVE CSV
# ----------------------------------------------------

df = pd.DataFrame(rows)

df.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 50)
print(f"Saved {len(df)} OCR words")
print(f"Output: {OUTPUT_CSV}")
print("=" * 50)

# ----------------------------------------------------
# SHOW CONFIDENCE STATISTICS
# ----------------------------------------------------

print("\nConfidence Statistics")
print(df["confidence"].describe())

print("\nWords with confidence < 50 :", (df["confidence"] < 50).sum())
print("Words with confidence < 60 :", (df["confidence"] < 60).sum())
print("Words with confidence < 70 :", (df["confidence"] < 70).sum())
print("Words with confidence < 80 :", (df["confidence"] < 80).sum())
print("Words with confidence < 90 :", (df["confidence"] < 90).sum())