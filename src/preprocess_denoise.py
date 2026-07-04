import cv2
import os

RAW_DIR = "../images"
PREPROCESSED_DIR = "../images_preprocessed_denoised"
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def preprocess_image(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Denoise
    img = cv2.fastNlMeansDenoising(img, h=15)
    cv2.imwrite(out_path, img)

def run_preprocess():
    for fname in sorted(os.listdir(RAW_DIR)):
        preprocess_image(f"{RAW_DIR}/{fname}", f"{PREPROCESSED_DIR}/{fname}")

if __name__ == "__main__":
    run_preprocess()