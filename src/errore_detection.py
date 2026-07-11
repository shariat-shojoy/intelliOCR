import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGES_DIR = "../images_preprocessed_denoised"  # your denoised images
DICT_PATH = "../bangla_academi_words.txt"  # your unique Bangla words dictionary
CONF_THRESHOLD = 90  # tune later

with open(DICT_PATH, encoding="utf-8") as f:
    BANGLA_DICT = set(line.strip() for line in f)

def get_words_with_confidence(image_path):
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, lang='ben', output_type=pytesseract.Output.DICT)
    words = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        conf = int(data['conf'][i])
        if text:
            words.append((text, conf))
    return words

import re
import string

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"

def clean_word(word):
    # strip punctuation from both ends
    return word.strip(string.punctuation + "।,;:!?\"'()[]/%")

def is_number(word):
    return all(ch in BANGLA_DIGITS + "0123456789." for ch in word) and len(word) > 0

def flag_word(word, conf):
    cleaned = clean_word(word)
    if is_number(cleaned):
        oov = False  # don't OOV-check numbers
    else:
        oov = cleaned not in BANGLA_DICT and cleaned != ""
    low_conf = conf < CONF_THRESHOLD
    return low_conf or oov, low_conf, oov

def process_page(image_path):
    words = get_words_with_confidence(image_path)
    flagged = []
    for word, conf in words:
        is_flagged, low_conf, oov = flag_word(word, conf)
        flagged.append({"word": word, "conf": conf, "flagged": is_flagged, "low_conf": low_conf, "oov": oov})
    return flagged

if __name__ == "__main__":
    for fname in sorted(os.listdir(IMAGES_DIR))[:5]:
        print(f"\n--- {fname} ---")
        result = process_page(f"{IMAGES_DIR}/{fname}")
        flagged_count = sum(1 for r in result if r["flagged"])
        low_conf_count = sum(1 for r in result if r["low_conf"])
        oov_count = sum(1 for r in result if r["oov"])
        print(f"Total: {len(result)}, Flagged: {flagged_count}, LowConf: {low_conf_count}, OOV: {oov_count}")

        for r in result:
            if r["flagged"]:
                reason = "low_conf" if r["low_conf"] else "oov"
                print(f"  {r['word']!r} conf={r['conf']} reason={reason}")