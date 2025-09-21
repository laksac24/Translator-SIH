import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def extract_text(image_path):
    """
    Extracts text using both Nepali and Sinhala, returns the one with higher confidence.
    """
    try:
        img = Image.open(image_path)
        
        # Get confidence data for both languages
        nepali_data = pytesseract.image_to_data(img, lang="nep", output_type=pytesseract.Output.DICT)
        sinhala_data = pytesseract.image_to_data(img, lang="sin", output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence (ignoring -1 values)
        nepali_conf = [int(c) for c in nepali_data['conf'] if int(c) > 0]
        sinhala_conf = [int(c) for c in sinhala_data['conf'] if int(c) > 0]
        
        nepali_avg = sum(nepali_conf) / len(nepali_conf) if nepali_conf else 0
        sinhala_avg = sum(sinhala_conf) / len(sinhala_conf) if sinhala_conf else 0
        
        # Use the language with higher confidence
        if nepali_avg >= sinhala_avg:
            text = pytesseract.image_to_string(img, lang="nep").strip()
            print(f"Language: Nepali (confidence: {nepali_avg:.1f})")
        else:
            text = pytesseract.image_to_string(img, lang="sin").strip()
            print(f"Language: Sinhala (confidence: {sinhala_avg:.1f})")
        
        return text
        
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage:
# result = extract_text("test_data/sample.png")
# print("Text:", result)