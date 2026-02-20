import psycopg2
import os
import streamlit as st
from embeddings import get_embedding

DB_URL = st.secrets["Database_URL"]


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

    cached = get_cached_embedding(content)

    if cached:
        return  # Already embedded ✅

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

def get_cached_embedding(content):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT embedding FROM knowledge WHERE content = %s LIMIT 1",
        (content,)
    )

    row = cur.fetchone()
    conn.close()

    return row[0] if row else None

