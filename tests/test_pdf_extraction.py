import os
from app.services.pdf_service import extract_text_from_pdf

# The target file we just added to the root directory
TEST_FILE = "test_cv.pdf"

def run_sanity_check():
    if not os.path.exists(TEST_FILE):
        print(f"❌ Error: Could not find '{TEST_FILE}' in the root directory.")
        return

    print(f"📄 Loading '{TEST_FILE}' into memory...")
    
    # Read the file as raw binary to simulate the FastAPI UploadFile behavior
    with open(TEST_FILE, "rb") as f:
        pdf_bytes = f.read()

    try:
        print("⚙️ Extracting text with layout preservation...\n")
        print("=" * 60)
        
        # Execute our isolated function
        extracted_text = extract_text_from_pdf(pdf_bytes)
        
        print(extracted_text)
        print("=" * 60)
        
        print(f"✅ Success! Extracted {len(extracted_text)} characters.")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    run_sanity_check()