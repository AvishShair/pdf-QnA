"""Premium UI Components for PDF Q&A Bot with Glassmorphism Design"""

import streamlit as st
from typing import List, Dict, Optional
import time


def get_premium_css(theme: str = "light") -> str:
    """
    Get premium CSS with glassmorphism, gradients, and animations
    
    Args:
        theme: 'light' or 'dark'
        
    Returns:
        CSS string
    """
    if theme == "dark":
        return """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            /* Root Variables */
            :root {
                --bg-primary: #0D0F16;
                --bg-secondary: rgba(255, 255, 255, 0.05);
                --bg-glass: rgba(255, 255, 255, 0.08);
                --text-primary: #ECECEC;
                --text-secondary: rgba(236, 236, 236, 0.7);
                --gradient-primary: linear-gradient(135deg, #6A5CFF 0%, #AD7BFF 100%);
                --gradient-accent: linear-gradient(135deg, #39F3C7 0%, #6A5CFF 100%);
                --glow-primary: rgba(147, 102, 255, 0.25);
                --shadow-soft: rgba(0, 0, 0, 0.3);
            }
            
            /* Global Styles */
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            
            .stApp {
                background: var(--bg-primary);
                background-image: 
                    radial-gradient(at 20% 30%, rgba(106, 92, 255, 0.15) 0px, transparent 50%),
                    radial-gradient(at 80% 70%, rgba(173, 123, 255, 0.15) 0px, transparent 50%);
            }
            
            /* Premium Header */
            .premium-header {
                font-size: 3.5rem;
                font-weight: 800;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 2rem 0 0.5rem 0;
                letter-spacing: -0.02em;
                animation: fadeInDown 0.6s ease-out;
            }
            
            .premium-subheader {
                font-size: 1.1rem;
                color: var(--text-secondary);
                text-align: center;
                margin-bottom: 3rem;
                font-weight: 400;
                animation: fadeInUp 0.6s ease-out 0.2s both;
            }
            
            /* Glass Cards */
            .glass-card {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px var(--shadow-soft);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                animation: fadeIn 0.5s ease-out;
            }
            
            .glass-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 40px var(--shadow-soft);
                border-color: rgba(106, 92, 255, 0.3);
            }
            
            /* Chat Bubbles */
            .chat-bubble-user {
                background: var(--gradient-primary);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 20px 20px 4px 20px;
                margin: 1rem 0;
                max-width: 75%;
                margin-left: auto;
                box-shadow: 0 4px 20px var(--glow-primary);
                animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 400;
                line-height: 1.6;
            }
            
            .chat-bubble-assistant {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                color: var(--text-primary);
                padding: 1rem 1.5rem;
                border-radius: 20px 20px 20px 4px;
                margin: 1rem 0;
                max-width: 75%;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 20px var(--shadow-soft);
                animation: slideInLeft 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 400;
                line-height: 1.6;
            }
            
            /* Premium Buttons */
            .premium-button {
                background: var(--gradient-primary);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 15px var(--glow-primary);
                position: relative;
                overflow: hidden;
            }
            
            .premium-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 25px var(--glow-primary);
            }
            
            .premium-button:active {
                transform: translateY(0) scale(0.98);
            }
            
            /* Citation Cards */
            .citation-card {
                background: var(--bg-glass);
                backdrop-filter: blur(15px) saturate(180%);
                border-radius: 16px;
                padding: 1.25rem;
                margin: 0.75rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 16px var(--shadow-soft);
                transition: all 0.3s ease;
                animation: fadeInUp 0.4s ease-out;
            }
            
            .citation-card:hover {
                transform: translateY(-2px);
                border-color: rgba(106, 92, 255, 0.3);
                box-shadow: 0 6px 24px var(--shadow-soft);
            }
            
            .page-badge {
                display: inline-block;
                background: var(--gradient-primary);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 0.5rem;
            }
            
            /* Progress Bar */
            .premium-progress {
                background: var(--bg-glass);
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                position: relative;
            }
            
            .premium-progress-fill {
                background: var(--gradient-primary);
                height: 100%;
                border-radius: 10px;
                transition: width 0.3s ease;
                box-shadow: 0 0 10px var(--glow-primary);
            }
            
            /* Upload Zone */
            .upload-zone {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                border: 2px dashed rgba(106, 92, 255, 0.4);
                border-radius: 20px;
                padding: 3rem 2rem;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .upload-zone:hover {
                border-color: rgba(106, 92, 255, 0.7);
                background: rgba(106, 92, 255, 0.1);
                transform: scale(1.02);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background: var(--bg-secondary);
                backdrop-filter: blur(20px) saturate(180%);
            }
            
            /* Metric Cards */
            .metric-card {
                background: var(--bg-glass);
                backdrop-filter: blur(15px);
                border-radius: 16px;
                padding: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            
            /* Typing Indicator */
            .typing-indicator {
                display: inline-flex;
                gap: 0.3rem;
                padding: 0.5rem 0;
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--text-secondary);
                animation: typing 1.4s infinite;
            }
            
            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.5;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
        </style>
        """
    else:  # Light theme
        return """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            /* Root Variables */
            :root {
                --bg-primary: #F7F9FC;
                --bg-secondary: rgba(255, 255, 255, 0.6);
                --bg-glass: rgba(255, 255, 255, 0.55);
                --text-primary: #1B1B1B;
                --text-secondary: rgba(27, 27, 27, 0.6);
                --gradient-primary: linear-gradient(135deg, #6A5CFF 0%, #AD7BFF 100%);
                --gradient-accent: linear-gradient(135deg, #39F3C7 0%, #6A5CFF 100%);
                --glow-primary: rgba(106, 92, 255, 0.2);
                --shadow-soft: rgba(0, 0, 0, 0.08);
            }
            
            /* Global Styles */
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            
            .stApp {
                background: var(--bg-primary);
                background-image: 
                    radial-gradient(at 20% 30%, rgba(106, 92, 255, 0.08) 0px, transparent 50%),
                    radial-gradient(at 80% 70%, rgba(173, 123, 255, 0.08) 0px, transparent 50%);
            }
            
            /* Premium Header */
            .premium-header {
                font-size: 3.5rem;
                font-weight: 800;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 2rem 0 0.5rem 0;
                letter-spacing: -0.02em;
                animation: fadeInDown 0.6s ease-out;
            }
            
            .premium-subheader {
                font-size: 1.1rem;
                color: var(--text-secondary);
                text-align: center;
                margin-bottom: 3rem;
                font-weight: 400;
                animation: fadeInUp 0.6s ease-out 0.2s both;
            }
            
            /* Glass Cards */
            .glass-card {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.5);
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px var(--shadow-soft);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                animation: fadeIn 0.5s ease-out;
            }
            
            .glass-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 40px var(--shadow-soft);
                border-color: rgba(106, 92, 255, 0.3);
            }
            
            /* Chat Bubbles */
            .chat-bubble-user {
                background: var(--gradient-primary);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 20px 20px 4px 20px;
                margin: 1rem 0;
                max-width: 75%;
                margin-left: auto;
                box-shadow: 0 4px 20px var(--glow-primary);
                animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 400;
                line-height: 1.6;
            }
            
            .chat-bubble-assistant {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                color: var(--text-primary);
                padding: 1rem 1.5rem;
                border-radius: 20px 20px 20px 4px;
                margin: 1rem 0;
                max-width: 75%;
                border: 1px solid rgba(255, 255, 255, 0.6);
                box-shadow: 0 4px 20px var(--shadow-soft);
                animation: slideInLeft 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 400;
                line-height: 1.6;
            }
            
            /* Premium Buttons */
            .premium-button {
                background: var(--gradient-primary);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 15px var(--glow-primary);
                position: relative;
                overflow: hidden;
            }
            
            .premium-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 25px var(--glow-primary);
            }
            
            .premium-button:active {
                transform: translateY(0) scale(0.98);
            }
            
            /* Citation Cards */
            .citation-card {
                background: var(--bg-glass);
                backdrop-filter: blur(15px) saturate(180%);
                border-radius: 16px;
                padding: 1.25rem;
                margin: 0.75rem 0;
                border: 1px solid rgba(255, 255, 255, 0.5);
                box-shadow: 0 4px 16px var(--shadow-soft);
                transition: all 0.3s ease;
                animation: fadeInUp 0.4s ease-out;
            }
            
            .citation-card:hover {
                transform: translateY(-2px);
                border-color: rgba(106, 92, 255, 0.3);
                box-shadow: 0 6px 24px var(--shadow-soft);
            }
            
            .page-badge {
                display: inline-block;
                background: var(--gradient-primary);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 0.5rem;
            }
            
            /* Progress Bar */
            .premium-progress {
                background: var(--bg-glass);
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                position: relative;
            }
            
            .premium-progress-fill {
                background: var(--gradient-primary);
                height: 100%;
                border-radius: 10px;
                transition: width 0.3s ease;
                box-shadow: 0 0 10px var(--glow-primary);
            }
            
            /* Upload Zone */
            .upload-zone {
                background: var(--bg-glass);
                backdrop-filter: blur(20px) saturate(180%);
                border: 2px dashed rgba(106, 92, 255, 0.4);
                border-radius: 20px;
                padding: 3rem 2rem;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .upload-zone:hover {
                border-color: rgba(106, 92, 255, 0.7);
                background: rgba(106, 92, 255, 0.1);
                transform: scale(1.02);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background: var(--bg-secondary);
                backdrop-filter: blur(20px) saturate(180%);
            }
            
            /* Metric Cards */
            .metric-card {
                background: var(--bg-glass);
                backdrop-filter: blur(15px);
                border-radius: 16px;
                padding: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.5);
                text-align: center;
            }
            
            /* Typing Indicator */
            .typing-indicator {
                display: inline-flex;
                gap: 0.3rem;
                padding: 0.5rem 0;
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--text-secondary);
                animation: typing 1.4s infinite;
            }
            
            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.5;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
        </style>
        """


def render_chat_message(role: str, content: str, sources: Optional[List[Dict]] = None):
    """
    Render a premium chat message with glassmorphism styling
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        sources: Optional list of sources
    """
    if role == "user":
        st.markdown(
            f'<div class="chat-bubble-user">{content}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble-assistant">{content}</div>',
            unsafe_allow_html=True
        )
        
        # Display sources if available
        if sources and len(sources) > 0:
            with st.expander("📚 Cited References", expanded=False):
                for source in sources:
                    render_citation_card(source)


def render_citation_card(source: Dict):
    """Render a premium citation card"""
    page_num = source.get('page', 0)
    filename = source.get('filename', 'Unknown')
    relevance = source.get('relevance_percent', 0)
    snippet = source.get('snippet', source.get('text', ''))[:300]
    
    st.markdown(
        f'''
        <div class="citation-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <span class="page-badge">Page {page_num}</span>
                <strong style="flex: 1;">{filename}</strong>
                <span style="color: #6A5CFF; font-weight: 600;">{relevance}% match</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; margin: 0;">
                {snippet}...
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )


def render_source_citations(sources: List[Dict], expanded: bool = False):
    """
    Render source citations section with premium styling
    
    Args:
        sources: List of source dictionaries
        expanded: Whether to expand by default
    """
    if not sources:
        return
    
    with st.expander("📚 Cited References", expanded=expanded):
        for source in sources:
            render_citation_card(source)


def render_sidebar_stats(
    total_pdfs: int,
    total_chunks: int,
    total_pages: int,
    embedding_progress: Optional[float] = None
):
    """
    Render premium sidebar statistics
    
    Args:
        total_pdfs: Number of PDFs loaded
        total_chunks: Number of chunks created
        total_pages: Total pages processed
        embedding_progress: Optional progress (0-1)
    """
    st.sidebar.markdown("### 📊 Statistics")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div style="font-size: 1.5rem; font-weight: 700; color: #6A5CFF;">{total_pdfs}</div><div style="font-size: 0.85rem; color: var(--text-secondary);">PDFs</div></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div style="font-size: 1.5rem; font-weight: 700; color: #6A5CFF;">{total_pages}</div><div style="font-size: 0.85rem; color: var(--text-secondary);">Pages</div></div>',
            unsafe_allow_html=True
        )
    
    st.markdown(
        f'<div class="metric-card"><div style="font-size: 1.5rem; font-weight: 700; color: #6A5CFF;">{total_chunks}</div><div style="font-size: 0.85rem; color: var(--text-secondary);">Chunks</div></div>',
        unsafe_allow_html=True
    )
    
    if embedding_progress is not None:
        st.markdown(
            f'''
            <div class="premium-progress" style="margin-top: 1rem;">
                <div class="premium-progress-fill" style="width: {embedding_progress * 100}%;"></div>
            </div>
            <p style="text-align: center; font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem;">
                Embedding: {int(embedding_progress * 100)}%
            </p>
            ''',
            unsafe_allow_html=True
        )


def render_history_panel(chat_history: List[Dict]):
    """
    Render premium chat history panel
    
    Args:
        chat_history: List of chat messages
    """
    if not chat_history:
        st.sidebar.markdown(
            '<div class="glass-card" style="text-align: center; padding: 2rem;"><p style="color: var(--text-secondary);">No chat history yet</p></div>',
            unsafe_allow_html=True
        )
        return
    
    st.sidebar.markdown("### 💬 Chat History")
    
    # Show last 10 messages
    for i, msg in enumerate(chat_history[-10:], 1):
        role = msg.get('role', 'user')
        content = msg.get('content', '')[:50] + "..." if len(msg.get('content', '')) > 50 else msg.get('content', '')
        
        if role == 'user':
            st.sidebar.markdown(
                f'<div class="glass-card" style="padding: 0.75rem; margin: 0.5rem 0;"><strong style="color: #6A5CFF;">Q{i}:</strong> <span style="color: var(--text-secondary);">{content}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.sidebar.markdown(
                f'<div class="glass-card" style="padding: 0.75rem; margin: 0.5rem 0;"><em style="color: var(--text-secondary);">A{i}:</em> <span style="color: var(--text-secondary);">{content[:30]}...</span></div>',
                unsafe_allow_html=True
            )
    
    if len(chat_history) > 10:
        st.sidebar.caption(f"... and {len(chat_history) - 10} more messages")


def render_summarization_buttons():
    """
    Render premium summarization action buttons
    
    Returns:
        Dictionary with button states
    """
    st.markdown("### 📝 Summarization Tools")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        summarize_full = st.button("📄 Summarize Entire PDF", use_container_width=True, type="primary")
    
    with col2:
        summarize_pages = st.button("📑 Summarize Selected Pages", use_container_width=True, type="secondary")
    
    with col3:
        key_points = st.button("🔑 Generate Key Points", use_container_width=True, type="primary")
    
    with col4:
        glossary = st.button("📖 Generate Glossary", use_container_width=True, type="secondary")
    
    return {
        'summarize_full': summarize_full,
        'summarize_pages': summarize_pages,
        'key_points': key_points,
        'glossary': glossary
    }


def render_progress_bar(stage: str, progress: float):
    """
    Render premium progress bar for processing stages
    
    Args:
        stage: Stage name
        progress: Progress (0-1)
    """
    st.markdown(
        f'''
        <div class="premium-progress" style="margin: 1rem 0;">
            <div class="premium-progress-fill" style="width: {progress * 100}%;"></div>
        </div>
        <p style="text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
            {stage}: {int(progress * 100)}%
        </p>
        ''',
        unsafe_allow_html=True
    )


def render_error_message(error: str, details: Optional[str] = None):
    """
    Render premium error message
    
    Args:
        error: Error message
        details: Optional detailed error information
    """
    st.markdown(
        f'<div class="glass-card" style="border-left: 4px solid #FF6B6B; background: rgba(255, 107, 107, 0.1);"><strong style="color: #FF6B6B;">❌ {error}</strong></div>',
        unsafe_allow_html=True
    )
    if details:
        with st.expander("Error Details"):
            st.code(details)


def render_success_message(message: str):
    """
    Render premium success message
    
    Args:
        message: Success message
    """
    st.markdown(
        f'<div class="glass-card" style="border-left: 4px solid #39F3C7; background: rgba(57, 243, 199, 0.1);"><strong style="color: #39F3C7;">✅ {message}</strong></div>',
        unsafe_allow_html=True
    )


def render_info_message(message: str):
    """
    Render premium info message
    
    Args:
        message: Info message
    """
    st.markdown(
        f'<div class="glass-card" style="border-left: 4px solid #6A5CFF; background: rgba(106, 92, 255, 0.1);"><strong style="color: #6A5CFF;">ℹ️ {message}</strong></div>',
        unsafe_allow_html=True
    )


def render_warning_message(message: str):
    """
    Render premium warning message
    
    Args:
        message: Warning message
    """
    st.markdown(
        f'<div class="glass-card" style="border-left: 4px solid #FFA726; background: rgba(255, 167, 38, 0.1);"><strong style="color: #FFA726;">⚠️ {message}</strong></div>',
        unsafe_allow_html=True
    )


def render_streaming_message(placeholder, content_so_far: str):
    """
    Update streaming message placeholder with typing indicator
    
    Args:
        placeholder: Streamlit placeholder
        content_so_far: Accumulated content
    """
    typing_indicator = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>'
    placeholder.markdown(
        f'<div class="chat-bubble-assistant">{content_so_far}<span style="opacity: 0.5;">▌</span></div>',
        unsafe_allow_html=True
    )


def get_custom_css(theme: str = "light") -> str:
    """
    Get premium CSS (wrapper for get_premium_css)
    
    Args:
        theme: 'light' or 'dark'
        
    Returns:
        CSS string
    """
    return get_premium_css(theme)


def render_theme_toggle():
    """Render theme toggle button (placeholder for future implementation)"""
    pass
