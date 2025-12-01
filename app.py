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
    render_warning_message, get_premium_css, render_welcome_screen,
    render_copy_button, render_stats_card
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

/* Floating Action Button */
.fab {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6A5CFF 0%, #AD7BFF 100%);
    box-shadow: 0 8px 24px rgba(106, 92, 255, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    animation: fabPulse 2s ease-in-out infinite;
}

.fab:hover {
    transform: scale(1.1) rotate(90deg);
    box-shadow: 0 12px 32px rgba(106, 92, 255, 0.5);
}

@keyframes fabPulse {
    0%, 100% { box-shadow: 0 8px 24px rgba(106, 92, 255, 0.4); }
    50% { box-shadow: 0 12px 36px rgba(106, 92, 255, 0.6); }
}

/* Smooth Scroll */
html {
    scroll-behavior: smooth;
}

/* Interactive hover effects */
.interactive-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(106, 92, 255, 0.2);
}
</style>

<div class="bg-blob bg-blob-1"></div>
<div class="bg-blob bg-blob-2"></div>
<div class="bg-blob bg-blob-3"></div>
""", unsafe_allow_html=True)

# Add keyboard shortcuts info
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus on chat input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const chatInput = document.querySelector('textarea[aria-label="Ask something about your documents..."]');
        if (chatInput) chatInput.focus();
    }
});
</script>
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
        "show_fab_menu": False,
        "processing_stage": "",
        "processing_progress": 0.0,
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
        
        # Stage 1: Extraction
        st.session_state.processing_stage = "Extracting text from PDFs"
        st.session_state.processing_progress = 0.2

        progress_bar = st.progress(0.2, text="📄 Extracting text...")
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

        # Stage 2: Chunking
        st.session_state.processing_stage = "Chunking text"
        st.session_state.processing_progress = 0.5
        progress_bar.progress(0.5, text="🔪 Chunking text...")
        
        chunk_size = 1400 if fast_mode else 900
        overlap = 20 if fast_mode else 50

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

        # Stage 3: Embeddings
        st.session_state.processing_stage = "Creating embeddings"
        st.session_state.processing_progress = 0.8
        progress_bar.progress(0.8, text="🧠 Creating embeddings...")
        
        embedder = EnhancedEmbedder(api_key)

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

        # Stage 4: Complete
        st.session_state.processing_stage = "Complete"
        st.session_state.processing_progress = 1.0
        progress_bar.progress(1.0, text="✅ Processing complete!")
        time.sleep(0.5)
        progress_bar.empty()
        
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
        st.markdown('<div style="text-align: center; margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 1.8rem; font-weight: 700; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">🤖 Control Panel</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Theme toggle with better styling
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div style="padding: 0.5rem 0; color: var(--text-primary); font-weight: 500;">☀️ Theme: {st.session_state.theme.title()}</div>', unsafe_allow_html=True)
        with col2:
            if st.button("🔄", use_container_width=True, help="Toggle theme"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()

        st.divider()
        
        # Collapsible API Key Section
        with st.expander("🔑 API Configuration", expanded=not bool(os.getenv("GOOGLE_API_KEY"))):
            api_key = get_api_key()
        
        if not os.getenv("GOOGLE_API_KEY"):
            api_key = st.session_state.get("api_key", "")
        else:
            api_key = os.getenv("GOOGLE_API_KEY")

        st.divider()
        
        # File Upload Section with enhanced UI
        st.markdown('📤 **Upload Documents**')
        uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

        with st.expander("⚙️ Advanced Options", expanded=False):
            use_ocr = st.checkbox("🔍 OCR for Scanned PDFs", False, help="Enable OCR for image-based PDFs")
            extract_tables = st.checkbox("📊 Extract Tables", True, help="Extract and process tables")
            extract_images = st.checkbox("🖼️ Extract Images", False, help="Extract images from PDFs")
            fast_mode = st.checkbox("⚡ Fast Mode", True, help="Faster processing with larger chunks")

        if uploaded_files and api_key:
            if st.button("🚀 Process PDFs", use_container_width=True, type="primary"):
                st.session_state.chat_history = []
                success = process_pdfs(
                    uploaded_files, api_key,
                    use_ocr=use_ocr,
                    extract_tables=extract_tables,
                    extract_images=extract_images,
                    fast_mode=fast_mode,
                )
                if success:
                    st.rerun()
        
        if uploaded_files and not api_key:
            render_warning_message("⚠️ Please provide API key above")

        st.divider()

        # Enhanced Statistics Section
        if st.session_state.processing_complete:
            st.markdown('📊 **Document Statistics**')
            
            # Use the new render_stats_card for better visuals
            col1, col2 = st.columns(2)
            with col1:
                render_stats_card(
                    title="PDFs",
                    value=str(len(st.session_state.uploaded_files_names)),
                    icon="📄",
                    color="#6A5CFF"
                )
            with col2:
                render_stats_card(
                    title="Pages",
                    value=str(st.session_state.total_pages),
                    icon="📚",
                    color="#39F3C7"
                )
            
            render_stats_card(
                title="Text Chunks",
                value=str(len(st.session_state.all_chunks)),
                icon="🧩",
                color="#AD7BFF"
            )
            
            # Quick Actions
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat", use_container_width=True, help="Clear conversation history"):
                st.session_state.chat_history = []
                st.rerun()

        st.divider()
        
        # Chat History with Collapsible Section
        with st.expander("💬 Chat History", expanded=False):
            render_history_panel(st.session_state.chat_history)

    # MAIN CONTENT
    if not st.session_state.processing_complete:
        # Show engaging welcome screen
        render_welcome_screen()
        return

    # Quick Action Buttons
    st.markdown('<div style="margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Summarize All", use_container_width=True, help="Generate full document summary"):
            handle_summarization("full")
    
    with col2:
        if st.button("🔑 Key Points", use_container_width=True, help="Extract key insights"):
            handle_summarization("key_points")
    
    with col3:
        if st.button("📖 Glossary", use_container_width=True, help="Generate term glossary"):
            handle_summarization("glossary")
    
    with col4:
        if st.button("💾 Export Chat", use_container_width=True, help="Download conversation"):
            if st.session_state.chat_history:
                chat_text = "\n\n".join([
                    f"{msg['role'].upper()}: {msg['content']}"
                    for msg in st.session_state.chat_history
                ])
                st.download_button(
                    label="⬇️ Download",
                    data=chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    st.markdown('</div>', unsafe_allow_html=True)
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

    # Chat input with keyboard shortcut hint
    st.markdown('<div style="text-align: center; color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem;">💡 Tip: Press <kbd>Ctrl+K</kbd> to focus on chat input</div>', unsafe_allow_html=True)
    user_question = st.chat_input("Ask something about your documents...")
    if user_question:
        handle_question(user_question)
    
    # Floating Action Button (FAB) for quick actions
    if st.session_state.processing_complete:
        st.markdown("""
        <div class="fab" title="Quick Actions" onclick="alert('Quick Actions: \\n1. Export Chat\\n2. Clear History\\n3. New Question')">
            <span style="font-size: 1.5rem; color: white;">⚡</span>
        </div>
        """, unsafe_allow_html=True)


# Run app
if __name__ == "__main__":
    main()
