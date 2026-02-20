from metadata import extract_metadata
from rag import extract_text_from_pdf, chunk_text
from db import save_knowledge

def ingest_pdf(pdf_file):

    metadata = extract_metadata(pdf_file)

    text = extract_text_from_pdf(pdf_file)
    chunks = chunk_text(text)

    for chunk in chunks:
        save_knowledge(chunk)

    return metadata, len(chunks)
