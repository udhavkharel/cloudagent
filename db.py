import psycopg2
import os
import streamlit as st
from embeddings import get_embedding
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL") or st.secrets["DATABASE_URL"]


def connect():
    return psycopg2.connect(DB_URL)


# ---------------- CHAT HISTORY ---------------- #

def save(role, message):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat_history (role, message) VALUES (%s, %s)",
        (role, message)
    )

    conn.commit()
    conn.close()


def load_history(limit=100):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT role, message FROM chat_history ORDER BY id DESC LIMIT %s",
        (limit,)
    )

    rows = cur.fetchall()
    conn.close()

    return rows[::-1]


# ---------------- KNOWLEDGE BASE (RAG) ---------------- #

def save_knowledge(content):
    embedding = get_embedding(content)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO knowledge (content, embedding) VALUES (%s, %s)",
        (content, embedding)
    )

    conn.commit()
    conn.close()


def search_knowledge(query):
    query_embedding = get_embedding(query)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT content
        FROM knowledge
        ORDER BY embedding <-> %s
        LIMIT 3
    """, (query_embedding,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]
