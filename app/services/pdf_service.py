import fitz  # PyMuPDF
import pymupdf4llm

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a CV PDF and converts it to Markdown, 
    strictly preserving column layouts and reading order.
    
    Args:
        file_bytes (bytes): The raw bytes of the uploaded PDF.
        
    Returns:
        str: The extracted text formatted as Markdown.
        
    Raises:
        ValueError: If the PDF cannot be read or contains no extractable text.
    """
    try:
        # Open the PDF directly from the byte stream
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        # Convert the document to Markdown
        # This handles columns, headers, and bullet points natively
        md_text = pymupdf4llm.to_markdown(doc)
        
        cleaned_text = md_text.strip()
        
        # The OCR Trap remains: Fail fast if the PDF is just an image
        if not cleaned_text:
            raise ValueError("The uploaded CV contains no readable text. It may be an image or a scanned document.")
            
        return cleaned_text
        
    except Exception as e:
        raise ValueError(f"Failed to process PDF: {str(e)}")