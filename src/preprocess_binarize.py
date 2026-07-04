import cv2
import os

RAW_DIR = "../images"
PREPROCESSED_DIR = "../images_preprocessed_binarized"
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def preprocess_image(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Binarize
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)

    cv2.imwrite(out_path, img)

def run_preprocess():
    for fname in sorted(os.listdir(RAW_DIR)):
        preprocess_image(f"{RAW_DIR}/{fname}", f"{PREPROCESSED_DIR}/{fname}")

if __name__ == "__main__":
    run_preprocess()