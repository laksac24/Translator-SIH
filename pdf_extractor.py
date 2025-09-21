import pdfplumber

def extract_nepali_sinhala_from_pdf(pdf_path):
    """
    Extracts Nepali and Sinhala text from a PDF using pdfplumber.
    Works only if the text is selectable (not scanned as images).

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Combined extracted text.
    """
    extracted_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

        return "\n".join(extracted_text).strip()

    except Exception as e:
        return f"Error: {str(e)}"


# Example usage
# result = extract_nepali_sinhala_from_pdf("test_data/sample6.pdf")
# print(result)
