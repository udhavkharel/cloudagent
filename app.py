import streamlit as st
from agent import chat
from pdf_ingest import ingest_pdf

st.title("📚 ResearchBuddy")

# ---- PDF Upload Section ----
uploaded_pdf = st.file_uploader(
    "Upload Research Paper (PDF)",
    type=["pdf"]
)

if uploaded_pdf:
    metadata, chunks = ingest_pdf(uploaded_pdf)

    st.success(f"✅ Ingested {chunks} chunks")
    st.write(f"**Title:** {metadata['title']}")
    st.write(f"**Author:** {metadata['author']}")

# ---- Chat Section ----
prompt = st.chat_input("Ask something about your research...")

if prompt:
    reply = chat(prompt)
    st.write(reply)
if uploaded_pdf:
    metadata, chunks = ingest_pdf(uploaded_pdf)
    st.success(...)
