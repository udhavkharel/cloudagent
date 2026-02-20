from openai import OpenAI
import os
import streamlit as st
from config import MODEL_NAME, SYSTEM_PROMPT
from db import save, load_history
from rag import retrieve_context
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
# Secure API key from Streamlit secrets
client = OpenAI(api_key=api_key)


def build_messages(prompt):
    history = load_history()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add previous chat history
    for role, msg in history:
        messages.append({"role": role, "content": msg})

    # Retrieve RAG context
    context, references = retrieve_context(prompt)

    if context:
        messages.append({
            "role": "system",
            "content": f"""
Use the following sources to answer the question.

Sources:
{context}

Rules:
- Base your answer primarily on the sources
- Cite using [Source X]
"""
        })

    # Add user prompt
    messages.append({"role": "user", "content": prompt})

    return messages, references


def ask_llm(prompt):
    messages, references = build_messages(prompt)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    reply = response.choices[0].message.content

    # Append references if RAG used
    if references:
        reply += "\n\n---\n📚 **References**\n"
        for ref in references:
            reply += f"- {ref}\n"

    return reply


def chat(prompt):
    reply = ask_llm(prompt)

    save("user", prompt)
    save("assistant", reply)

    return reply
