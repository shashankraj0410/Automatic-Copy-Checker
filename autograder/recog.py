import cv2
import pytesseract
import numpy as np
import logging
from spellchecker import SpellChecker
from PIL import Image, ImageEnhance, ImageOps

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("Image reading failed.")
    
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Perform adaptive thresholding to emphasize text regions
    binary_image = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    #  increase the contrast using histogram equalization
    equalized_image = cv2.equalizeHist(binary_image)

    # Apply morphological transformations to clean small noise
    kernel = np.ones((1, 1), np.uint8)
    morph_image = cv2.morphologyEx(equalized_image, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    #  Resize image to a fixed width while maintaining the aspect ratio (if OCR struggles with size)
    desired_width = 1024
    aspect_ratio = float(image.shape[1]) / float(image.shape[0])
    new_size = (desired_width, int(desired_width / aspect_ratio))
    resized_image = cv2.resize(morph_image, new_size)

    return resized_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_ocr(image_path):
    """
    Perform OCR using Tesseract on the preprocessed image and return the recognized text.
    Includes spell-checking on the recognized text.
    """
    try:
        # Read image from the provided path
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Image reading failed for {image_path}.")

        # Preprocess the image for better OCR performance
        preprocessed_image = preprocess_image(image_path)

        if preprocessed_image is None:
            raise ValueError("Image preprocessing failed.")

        # Perform OCR using Tesseract
        recognized_text = pytesseract.image_to_string(preprocessed_image, config='--psm 3')  # Change psm as needed

        if not recognized_text.strip():
            raise ValueError("No text recognized from the image.")

        # Correct spelling errors in the recognized text
        corrected_text = correct_spelling(recognized_text)

        logging.info(f"OCR Result (corrected): {corrected_text}")
        return corrected_text

    except Exception as e:
        logging.error(f"Error performing OCR on {image_path}: {e}")
        return None  # Returning None instead of empty string for clarity
def correct_spelling(text):
    """
    Correct spelling of the OCR output using the `SpellChecker` library.
    """
    if not text:
        return text

    try:
        spell = SpellChecker()
        corrected_words = []
        words = text.split()

        for word in words:
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word if corrected_word else word)

        return " ".join(corrected_words)

    except Exception as e:
        print(f"Error during spell-check: {e}")
        return text
