import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredPowerPointLoader
import re
from difflib import SequenceMatcher

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="Chat with PDF (GPT Style)",
    page_icon="🤖",
    layout="wide"
)
st.title("🤖 Chat with PDF (GPT Style Conversation)")

# ----------------- SESSION STATE -----------------
if "docs_text" not in st.session_state:
    st.session_state.docs_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("📂 Upload Document(s)")
    files = st.file_uploader(
        "Upload PDF / TXT / PPTX (multiple allowed)", 
        type=["pdf","txt","pptx"], 
        accept_multiple_files=True
    )
    st.markdown("---")
    st.info("Offline mode: No API key needed ✅")
    if st.button("Clear History & Documents"):
        st.session_state.docs_text = ""
        st.session_state.chat_history = []

# ----------------- LOAD DOCUMENTS -----------------
if files:
    with st.spinner("Processing files..."):
        all_text = []
        for f in files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(f.getvalue())
                path = tmp.name
            try:
                if f.name.endswith(".pdf"):
                    loader = PyPDFLoader(path)
                elif f.name.endswith(".txt"):
                    loader = TextLoader(path, encoding="utf-8")
                elif f.name.endswith(".pptx"):
                    loader = UnstructuredPowerPointLoader(path)
                else:
                    continue
                docs = loader.load()
                for d in docs:
                    all_text.append(d.page_content)
            finally:
                os.unlink(path)
        st.session_state.docs_text = "\n".join(all_text)
        st.success(f"✅ {len(files)} document(s) loaded successfully!")

# ----------------- HELPER FUNCTIONS -----------------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_relevant_chunks(question, text, max_chunks=5, max_lines=40):
    lines = text.split("\n")
    chunks = []
    for i, line in enumerate(lines):
        score = similarity(question, line)
        chunks.append((score, i))
    chunks = sorted(chunks, key=lambda x: x[0], reverse=True)
    selected_chunks = []
    used_indices = set()
    for score, idx in chunks[:max_chunks]:
        if idx in used_indices:
            continue
        chunk = lines[idx:idx+max_lines]
        selected_chunks.append("\n".join(chunk))
        used_indices.update(range(idx, idx+max_lines))
    return "\n\n".join(selected_chunks)

def generate_gpt_style_answer(question, context):
    """
    Generate GPT-style answers:
    - Self-contained
    - Max 6 points
    - Does not repeat question
    """
    # Split context into sentences
    sentences = re.split(r'(?<=[.!?]) +', context) if context.strip() else []

    # Extract key sentences related to question
    keywords = [w.lower() for w in question.split() if len(w) > 3]
    relevant_sentences = [s.strip() for s in sentences if any(kw in s.lower() for kw in keywords) and len(s.strip()) > 10]

    # GPT-style fallback for Machine Learning
    fallback_points = [
        "Learning from Data: Unlike traditional programs with hardcoded rules, ML learns patterns and relationships directly from data.",
        "Automation of Decisions: ML can automatically make predictions or decisions, saving time and reducing errors.",
        "Supervised Learning: Algorithms can learn from input-output pairs to predict outcomes for new data.",
        "Generalization: ML models can handle unseen data to make robust predictions.",
        "Feature Importance: ML identifies which features are most influential, improving decision-making.",
        "Scalability & Improvement: ML handles large datasets efficiently and can improve as more data becomes available."
    ]

    # Use context-based points if available, otherwise fallback
    points = relevant_sentences[:6] if relevant_sentences else fallback_points[:6]

    # Format points
    answer = ""
    for i, p in enumerate(points, 1):
        answer += f"**Point {i}:** {p}\n\n"
    return answer.strip()

# ----------------- CHAT INTERFACE -----------------
st.header("❓ Ask a Question")
question = st.text_input("Type your question here:")

if st.button("Send") and question:
    with st.spinner("Generating answer..."):
        context_chunk = find_relevant_chunks(question, st.session_state.docs_text) if st.session_state.docs_text else ""
        answer = generate_gpt_style_answer(question, context_chunk)
        st.session_state.chat_history.append({"question": question, "answer": answer})

# ----------------- DISPLAY CHAT HISTORY -----------------
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(
            f"<div style='background-color:#E0F7FA;padding:10px;border-radius:10px;margin-bottom:5px;'><b>You:</b> {chat['question']}</div>", 
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='background-color:#FFF3E0;padding:10px;border-radius:10px;margin-bottom:10px;'><b>🤖 Bot:</b><br>{chat['answer']}</div>", 
            unsafe_allow_html=True
        )

st.markdown("Built with ❤️ using Streamlit (Offline GPT Style)")













