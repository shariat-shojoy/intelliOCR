import cv2
import os

RAW_DIR = "../images"
PREPROCESSED_DIR = "../images_preprocessed_descewed"
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def preprocess_image(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Deskew
    coords = cv2.findNonZero(cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1])
    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    (h, w) = img.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite(out_path, img)

def run_preprocess():
    for fname in sorted(os.listdir(RAW_DIR)):
        preprocess_image(f"{RAW_DIR}/{fname}", f"{PREPROCESSED_DIR}/{fname}")

if __name__ == "__main__":
    run_preprocess()