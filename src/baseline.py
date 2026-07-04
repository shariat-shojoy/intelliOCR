import os
import easyocr
import pytesseract
from PIL import Image
import jiwer
from tqdm import tqdm
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


IMAGES_DIR = "../images_preprocessed_binarized"
GOLD_DIR = "../gold"
EASYOCR_OUT = "../output/easyocr_binarized"
TESSERACT_OUT = "../output/tesseract_binarized"

os.makedirs(EASYOCR_OUT, exist_ok=True)
os.makedirs(TESSERACT_OUT, exist_ok=True)

reader = easyocr.Reader(['bn'])

def ocr_easyocr(image_path):
    result = reader.readtext(image_path, detail=0, paragraph=True)
    return " ".join(result)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_tesseract(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang='ben')

def run_ocr():
    for fname in sorted(os.listdir(IMAGES_DIR)):
        img_path = os.path.join(IMAGES_DIR, fname)
        base = os.path.splitext(fname)[0]

        easy_text = ocr_easyocr(img_path)
        with open(f"{EASYOCR_OUT}/{base}.txt", "w", encoding="utf-8") as f:
            f.write(easy_text)

        tess_text = ocr_tesseract(img_path)
        with open(f"{TESSERACT_OUT}/{base}.txt", "w", encoding="utf-8") as f:
            f.write(tess_text)

        print(f"Processed {fname}")

def evaluate(ocr_dir, label):
    cer_scores, wer_scores = [], []
    for fname in sorted(os.listdir(GOLD_DIR)):
        gold_text = open(f"{GOLD_DIR}/{fname}", encoding="utf-8").read()
        ocr_path = f"{ocr_dir}/{fname}"
        if not os.path.exists(ocr_path):
            continue
        ocr_text = open(ocr_path, encoding="utf-8").read()
        cer_scores.append(jiwer.cer(gold_text, ocr_text))
        wer_scores.append(jiwer.wer(gold_text, ocr_text))
    print(f"\n[{label}] Mean CER: {sum(cer_scores)/len(cer_scores):.4f}")
    print(f"[{label}] Mean WER: {sum(wer_scores)/len(wer_scores):.4f}")

if __name__ == "__main__":
    run_ocr()
    evaluate(EASYOCR_OUT, "EasyOCR")
    evaluate(TESSERACT_OUT, "Tesseract")