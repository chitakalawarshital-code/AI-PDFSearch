import streamlit as st
import os
import tempfile
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredPowerPointLoader
)

# ----------------- CONFIG -----------------
load_dotenv()

st.set_page_config(
    page_title="AI Document Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Document Copilot")

# ----------------- SESSION STATE -----------------
if "lines" not in st.session_state:
    st.session_state.lines = []

if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False

if "last_chunk_size" not in st.session_state:
    st.session_state.last_chunk_size = 0

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("📂 Document Status / Upload")

    # --------------- FILE UPLOAD IN SIDEBAR ---------------
    files = st.file_uploader(
        "Browse Document (PDF / TXT / PPTX)",
        type=["pdf", "txt", "pptx"],
        accept_multiple_files=True
    )

    if st.session_state.doc_loaded:
        st.success("✅ Document Loaded Successfully")

        st.markdown("### 📦 Chunk Info")
        st.write(f"Total Chunks (Lines): **{len(st.session_state.lines)}**")
        st.write(f"Last Answer Chunk Size: **{st.session_state.last_chunk_size}**")

        if st.button("🗑️ Delete / Clear Document"):
            st.session_state.lines = []
            st.session_state.doc_loaded = False
            st.session_state.last_chunk_size = 0
            st.experimental_rerun()
    else:
        st.info("No document loaded yet")

# ----------------- LOAD DOCUMENT -----------------
if files:
    with st.spinner("Processing document..."):
        full_text = []

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
                    full_text.append(d.page_content)

            finally:
                os.unlink(path)

        raw_lines = "\n".join(full_text).split("\n")

        clean_lines = []
        stop_sections = {"index", "glossary", "references"}

        for line in raw_lines:
            line = line.strip()
            lower = line.lower()

            if lower in stop_sections:
                break

            if re.fullmatch(r"\d+", line):
                continue

            if re.search(r"\|\s*\d+$", line):
                continue

            if re.search(r",\s*\d", line) and line.count(",") >= 2:
                continue

            line = re.sub(r"^\d+[\.\)\-]\s*", "", line)

            if line:
                clean_lines.append(line)

        st.session_state.lines = clean_lines
        st.session_state.doc_loaded = True
        st.success("✅ Document processed and chunked successfully")

# ----------------- HELPERS -----------------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_heading(line):
    words = line.split()
    if len(words) < 2 or len(words) > 10:
        return False
    caps = sum(1 for w in words if w[0].isupper())
    return (caps / len(words)) >= 0.7

def find_best_chunk(question, lines):
    best_idx = 0
    best_score = 0.0

    for i, line in enumerate(lines):
        score = similarity(question, line)
        if score > best_score:
            best_score = score
            best_idx = i

    chunk = []
    for line in lines[best_idx + 1:]:
        if is_heading(line):
            break
        chunk.append(line)

    return chunk

# ----------------- QUESTION AREA -----------------
st.header("❓ Ask Question")

question = st.text_input("Ask anything from the document:")

if question and st.session_state.lines:
    with st.spinner("Finding best answer..."):
        chunk = find_best_chunk(question, st.session_state.lines)
        st.session_state.last_chunk_size = len(chunk)

        if chunk:
            st.subheader("✅ Answer")
            st.write(" ".join(chunk))  # <-- Shows answer in paragraph form
        else:
            st.info("ℹ️ No direct answer found")

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")





