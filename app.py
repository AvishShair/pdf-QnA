"""
Enhanced PDF Question-Answer Bot using Gemini AI
Advanced Streamlit application with:
- Multi-PDF support
- OCR for scanned PDFs
- Table & image extraction
- FAISS vector search
- Streaming responses
- Summaries & glossary generator
- Dark/Light theme toggle
- Floating animated background (Premium UI)
"""

import streamlit as st
import os
from dotenv import load_dotenv
from typing import List, Optional
import time

# Import core modules
from core.pdf_parser import EnhancedPDFParser
from core.embedder import EnhancedEmbedder
from core.retrieval import RetrievalEngine
from core.qa_engine import EnhancedQAEngine

# Import UI components
from ui.components import (
    render_chat_message, render_streaming_message, render_source_citations,
    render_sidebar_stats, render_history_panel, render_summarization_buttons,
    render_error_message, render_success_message, render_info_message,
    render_warning_message, get_premium_css
)

# Utilities
from utils.helpers import chunk_text_by_tokens

# Load environment variables
load_dotenv()

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="PDF Q&A Bot - Gemini AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# FLOATING ANIMATED BACKGROUND
# -------------------------------
st.markdown("""
<style>
.bg-blob {
    position: fixed;
    z-index: -1;
    filter: blur(90px);
    opacity: 0.35;
    animation: floatBlob 22s ease-in-out infinite alternate;
}

.bg-blob-1 {
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, #6A5CFF 0%, transparent 70%);
    top: -120px;
    left: -120px;
}

.bg-blob-2 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #39F3C7 0%, transparent 70%);
    bottom: -150px;
    right: -180px;
    animation-delay: 3s;
}

.bg-blob-3 {
    width: 360px;
    height: 360px;
    background: radial-gradient(circle, #AD7BFF 0%, transparent 75%);
    bottom: 40%;
    left: -170px;
    animation-duration: 26s;
}

@keyframes floatBlob {
    0% { transform: translate(0px, 0px) scale(1); }
    50% { transform: translate(60px, -40px) scale(1.25); }
    100% { transform: translate(-40px, 40px) scale(1); }
}
</style>

<div class="bg-blob bg-blob-1"></div>
<div class="bg-blob bg-blob-2"></div>
<div class="bg-blob bg-blob-3"></div>
""", unsafe_allow_html=True)



# -------------------------------
# THEME + CSS
# -------------------------------
def apply_theme():
    theme = st.session_state.get("theme", "light")
    st.markdown(get_premium_css(theme), unsafe_allow_html=True)

apply_theme()


# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
def initialize_session_state():
    defaults = {
        "chat_history": [],
        "pdf_data": [],
        "all_chunks": [],
        "embedder": None,
        "retrieval_engine": None,
        "qa_engine": None,
        "processing_complete": False,
        "uploaded_files_names": [],
        "total_pages": 0,
        "streaming_enabled": True,
        "theme": "light",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


initialize_session_state()


# -------------------------------
# API KEY HANDLER
# -------------------------------
def get_api_key() -> Optional[str]:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.sidebar.warning("⚠️ No API Key found.")
        user_key = st.sidebar.text_input(
            "Enter Google Gemini API Key", type="password"
        )
        if user_key:
            st.session_state["api_key"] = user_key
        return user_key

    return api_key



# -------------------------------
# PROCESS PDFS
# -------------------------------
def process_pdfs(uploaded_files, api_key, use_ocr=False, extract_tables=True, extract_images=False, fast_mode=True):

    try:
        parser = EnhancedPDFParser()

        with st.spinner("📄 Extracting text..."):
            files_data = [(f.name, f.read()) for f in uploaded_files]
            results = parser.extract_from_multiple_pdfs(
                files_data,
                use_ocr=use_ocr,
                extract_tables=extract_tables,
                extract_images=extract_images
            )

        success_results = [r for r in results if r["success"]]

        if not success_results:
            render_error_message("Failed to extract data from PDFs.")
            return False

        st.session_state.pdf_data = success_results
        st.session_state.uploaded_files_names = [r["filename"] for r in success_results]
        st.session_state.total_pages = sum(r.get("page_count", 0) for r in success_results)

        render_success_message(f"Successfully extracted {len(success_results)} PDFs.")

        # Chunking
        chunk_size = 1400 if fast_mode else 900
        overlap = 20 if fast_mode else 50

        with st.spinner("🔪 Chunking text..."):
            all_chunks = []
            for res in success_results:
                chunks = chunk_text_by_tokens(
                    res.get("text", ""),
                    chunk_size=chunk_size,
                    overlap=overlap,
                    metadata={"filename": res["filename"]}
                )
                all_chunks.extend(chunks)

        st.session_state.all_chunks = all_chunks

        # Embeddings
        embedder = EnhancedEmbedder(api_key)

        with st.spinner("🧠 Creating embeddings..."):
            texts = [c["text"] for c in all_chunks]
            metas = [c["metadata"] for c in all_chunks]
            embedder.create_embeddings(
                [{"text": t, "metadata": m} for t, m in zip(texts, metas)]
            )

        st.session_state.embedder = embedder
        st.session_state.retrieval_engine = RetrievalEngine(embedder)

        # QA engine
        qa = EnhancedQAEngine(api_key)
        qa.test_connection()
        st.session_state.qa_engine = qa

        st.session_state.processing_complete = True
        return True

    except Exception as e:
        render_error_message("❌ PDF Processing Failed", str(e))
        return False



# -------------------------------
# HANDLE QUESTION
# -------------------------------
def handle_question(question: str, stream=True):

    if not st.session_state.retrieval_engine:
        render_error_message("Please process PDFs first.")
        return

    st.session_state.chat_history.append({"role": "user", "content": question})
    render_chat_message("user", question)

    with st.spinner("🔍 Finding relevant information..."):
        context, sources = st.session_state.retrieval_engine.get_context_for_qa(
            question, top_k=5
        )

    if not sources:
        ans = "No relevant information found."
        render_chat_message("assistant", ans)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        return

    # Streaming mode
    if stream and st.session_state.streaming_enabled:
        placeholder = st.empty()
        full = ""
        try:
            for token in st.session_state.qa_engine.answer_question_stream(
                question, context, sources, st.session_state.chat_history[-10:]
            ):
                full += token
                render_streaming_message(placeholder, full)
                time.sleep(0.01)

            st.markdown(
                f'<div class="chat-bubble chat-bubble-assistant">{full}</div>',
                unsafe_allow_html=True,
            )
        except:
            result = st.session_state.qa_engine.answer_question(
                question, context, sources, st.session_state.chat_history[-10:]
            )
            full = result["answer"]
            placeholder.markdown(full)

    else:
        result = st.session_state.qa_engine.answer_question(
            question, context, sources, st.session_state.chat_history[-10:]
        )
        full = result["answer"]
        render_chat_message("assistant", full)

    render_source_citations(sources)
    st.session_state.chat_history.append({"role": "assistant", "content": full, "sources": sources})



# -------------------------------
# HANDLE SUMMARIES
# -------------------------------
def handle_summarization(summary_type: str):

    if not st.session_state.pdf_data:
        render_error_message("No PDFs loaded.")
        return

    qa = st.session_state.qa_engine
    if not qa:
        render_error_message("QA engine not initialized.")
        return

    all_text = "\n\n".join([r.get("text", "") for r in st.session_state.pdf_data])

    try:
        summary = qa.summarize(all_text, summary_type=summary_type)
        st.markdown("### 📝 Summary")
        st.markdown(summary)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": summary
        })
    except Exception as e:
        render_error_message("Summary error", str(e))



# -------------------------------
# MAIN APPLICATION
# -------------------------------
def main():
    initialize_session_state()

    # HEADER
    st.markdown('<div class="premium-header">PDF Question Answering Bot</div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-subheader">Powered by Google Gemini AI • Advanced Features</div>', unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:

        # Theme toggle
        if st.button("🌗 Toggle Theme", use_container_width=True):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.experimental_rerun()

        api_key = get_api_key()
        st.divider()

        uploaded_files = st.file_uploader("📤 Upload PDFs", type=["pdf"], accept_multiple_files=True)

        with st.expander("⚙️ Options"):
            use_ocr = st.checkbox("OCR (Scanned PDFs)", False)
            extract_tables = st.checkbox("Extract Tables", True)
            extract_images = st.checkbox("Extract Images", False)
            fast_mode = st.checkbox("Fast Mode (recommended)", True)

        if uploaded_files and api_key:
            if st.button("🚀 Process PDFs", use_container_width=True):
                st.session_state.chat_history = []
                success = process_pdfs(
                    uploaded_files, api_key,
                    use_ocr=use_ocr,
                    extract_tables=extract_tables,
                    extract_images=extract_images,
                    fast_mode=fast_mode,
                )
                if success:
                    st.experimental_rerun()

        st.divider()

        if st.session_state.processing_complete:
            render_sidebar_stats(
                total_pdfs=len(st.session_state.uploaded_files_names),
                total_chunks=len(st.session_state.all_chunks),
                total_pages=st.session_state.total_pages,
            )

        st.divider()
        render_history_panel(st.session_state.chat_history)

    # MAIN CONTENT
    if not st.session_state.processing_complete:
        render_info_message("👈 Upload PDFs to begin.")
        return

    # Summaries
    actions = render_summarization_buttons()
    if actions["summarize_full"]:
        handle_summarization("full")
    if actions["key_points"]:
        handle_summarization("key_points")
    if actions["glossary"]:
        handle_summarization("glossary")

    st.markdown("---")
    st.markdown("## 💬 Conversation")

    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="chat-glass">', unsafe_allow_html=True)

        for message in st.session_state.chat_history:
            render_chat_message(
                message.get("role"),
                message.get("content"),
                message.get("sources")
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    user_question = st.chat_input("Ask something about your documents...")
    if user_question:
        handle_question(user_question)


# Run app
if __name__ == "__main__":
    main()
