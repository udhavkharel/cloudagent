from pypdf import PdfReader
from db import save_knowledge
from rag import retrieve_context
from metadata import extract_metadata


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def ingest_pdf(pdf_file):

    metadata = extract_metadata(pdf_file)

    text = retrieve_context(pdf_file)
    chunks = chunk_text(text)

    for chunk in chunks:
        save_knowledge(chunk)

    return metadata, len(chunks)