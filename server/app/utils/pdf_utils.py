import PyPDF2

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        text_content = "".join(page.extract_text() for page in pdf_reader.pages)
        return text_content
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
