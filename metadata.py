from pypdf import PdfReader

def extract_metadata(pdf_file):

    reader = PdfReader(pdf_file)
    meta = reader.metadata

    return {
        "title": meta.title if meta.title else "Unknown Title",
        "author": meta.author if meta.author else "Unknown Author"
    }
