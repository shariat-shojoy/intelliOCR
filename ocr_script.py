import os
import easyocr
import pytesseract
from PIL import Image

# ==========================
# Configuration
# ==========================
IMAGE_DIR = "images"                 # Folder containing images
EASYOCR_OUT = "easyocr_output"       # Output folder for EasyOCR
TESSERACT_OUT = "tesseract_output"   # Output folder for Tesseract

# If Tesseract is not added to PATH, specify the executable via environment
# variable TESSERACT_CMD or by editing the default paths below.

# Helper to locate Tesseract on Windows.
def find_tesseract():
    import shutil
    # First try PATH / env var lookup
    env_path = os.environ.get('TESSERACT_CMD') or os.environ.get('TESSERACT_PATH')
    if env_path and os.path.isfile(env_path):
        return env_path
    if shutil.which('tesseract'):
        return shutil.which('tesseract')

    # Common Windows install locations
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    for path in common_paths:
        if os.path.isfile(path):
            return path
    return None

# Locate and configure the Tesseract executable before OCR
TESSERACT_CMD = find_tesseract()
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
else:
    raise SystemExit(
        "Tesseract is not installed or not found in PATH. "
        "Install Tesseract-OCR for Windows and add it to PATH, or set the "
        "environment variable TESSERACT_CMD to the full path of tesseract.exe. "
        "Example: C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )

# ==========================
# Create output folders
# ==========================
os.makedirs(EASYOCR_OUT, exist_ok=True)
os.makedirs(TESSERACT_OUT, exist_ok=True)

# ==========================
# Load EasyOCR once
# ==========================
reader = easyocr.Reader(['bn'])

# Supported image extensions
extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

# ==========================
# Process all images
# ==========================
for filename in sorted(os.listdir(IMAGE_DIR)):
    if not filename.lower().endswith(extensions):
        continue

    image_path = os.path.join(IMAGE_DIR, filename)

    print(f"Processing: {filename}")

    # --------------------------
    # EasyOCR
    # --------------------------
    easy_text = reader.readtext(
        image_path,
        detail=0,
        paragraph=True
    )
    easy_text = "\n".join(easy_text)

    easy_output_file = os.path.join(
        EASYOCR_OUT,
        os.path.splitext(filename)[0] + ".txt"
    )

    with open(easy_output_file, "w", encoding="utf-8") as f:
        f.write(easy_text)

    # --------------------------
    # Tesseract OCR
    # --------------------------
    image = Image.open(image_path)

    tess_text = pytesseract.image_to_string(
        image,
        lang='ben',
        config='--oem 3 --psm 6'
    )

    tess_output_file = os.path.join(
        TESSERACT_OUT,
        os.path.splitext(filename)[0] + ".txt"
    )

    with open(tess_output_file, "w", encoding="utf-8") as f:
        f.write(tess_text)

print("\nFinished OCR on all images.")