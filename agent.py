from openai import OpenAI
import streamlit as st
from config import MODEL_NAME, SYSTEM_PROMPT
from db import save, load_history
from rag import retrieve_context

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def build_messages(prompt):

    history = load_history()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for role, msg in history:
        messages.append({"role": role, "content": msg})

    context, references = retrieve_context(prompt)

    if context:
        messages.append({
            "role": "system",
            "content": f"""
Use the following sources to answer:

{context}

Cite sources using [Source X].
"""
        })

    messages.append({"role": "user", "content": prompt})

    return messages, references


def ask_llm(prompt):

    messages, references = build_messages(prompt)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    reply = response.choices[0].message.content

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
