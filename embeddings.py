from openai import OpenAI
import streamlit as st
import hashlib

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
