# 📄 Enhanced PDF Question-Answer Bot

**Production-ready PDF Q&A Bot with advanced features powered by Google Gemini AI and Streamlit**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-green.svg)](https://ai.google.dev)

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
echo "GOOGLE_API_KEY=your_key" > .env

# 3. Run app
streamlit run app.py
```

**That's it!** Open `http://localhost:8501` and start querying your PDFs.

---

## ✨ Key Features

### 🎯 Core Features
- ✅ **Multi-PDF Support** - Upload and query multiple PDFs simultaneously
- ✅ **Advanced Text Extraction** - pdfplumber + OCR for scanned PDFs
- ✅ **Table Extraction** - Extract and query tables from PDFs
- ✅ **Image Extraction** - Ready for vision-based Q&A
- ✅ **FAISS Vector Search** - Fast semantic similarity search
- ✅ **Relevance Scoring** - 0-100% relevance scores for sources
- ✅ **Page Number Tracking** - Citations include exact page numbers
- ✅ **Streaming Responses** - Real-time token-by-token generation
- ✅ **Chat Memory** - Context-aware follow-up questions
- ✅ **Summarization Tools** - 4 types of summaries

### 🎨 UI Features
- ✅ **Modern Interface** - Clean, professional design
- ✅ **Statistics Panel** - PDFs, pages, chunks tracking
- ✅ **History Panel** - Quick access to past questions
- ✅ **Source Citations** - Expandable references with highlights
- ✅ **Progress Indicators** - Real-time processing feedback
- ✅ **Error Handling** - User-friendly error messages

---

## 📁 Project Structure

```
pdfq&a/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
│
├── core/                       # Core functionality modules
│   ├── __init__.py
│   ├── pdf_parser.py          # Enhanced PDF parsing
│   ├── ocr.py                 # OCR for scanned PDFs
│   ├── embedder.py            # FAISS embeddings
│   ├── retrieval.py           # Semantic search
│   └── qa_engine.py           # QA with streaming
│
├── ui/                         # UI components
│   ├── __init__.py
│   └── components.py          # Reusable UI components
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   └── helpers.py             # Helper functions
│
└── Documentation/
    ├── README.md              # Main documentation
    ├── INSTALLATION.md        # Installation guide
    ├── ENHANCED_FEATURES.md   # Feature details
    ├── UPGRADE_GUIDE.md       # Upgrade instructions
    ├── USAGE_GUIDE.md         # User guide
    ├── DEPLOYMENT.md          # Deployment guide
    └── TESTING.md             # Testing procedures
```

---

## 🎯 Use Cases

### Research Papers
- "What were the main findings?"
- "Compare methodologies across papers"
- "What are the limitations mentioned?"

### Legal Documents
- "What are the key terms?"
- "What are the parties' obligations?"
- "What is the termination clause?"

### Technical Manuals
- "How do I configure X?"
- "What are the system requirements?"
- "How do I troubleshoot error Y?"

### Financial Reports
- "What was the revenue growth?"
- "What are the key metrics?"
- "What risks are mentioned?"

---

## 📦 Installation

### Basic Installation
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
echo "GOOGLE_API_KEY=your_key" > .env

# 4. Run
streamlit run app.py
```

### With OCR Support
```bash
# Install system dependencies
sudo apt-get install tesseract-ocr poppler-utils  # Ubuntu/Debian
brew install tesseract poppler                     # macOS

# Python packages are in requirements.txt
pip install -r requirements.txt
```

**See `INSTALLATION.md` for detailed instructions.**

---

## 🚀 Usage

### 1. Upload PDFs
- Click "Browse files" in sidebar
- Select one or more PDF files
- Choose processing options (OCR, tables, images)

### 2. Process PDFs
- Click "🚀 Process PDFs"
- Wait for processing (30-120 seconds)
- See progress indicators

### 3. Ask Questions
- Type question in chat input
- Press Enter
- View streaming response
- Check sources in "Cited References"

### 4. Use Summarization
- Click summarization buttons:
  - 📄 Summarize Entire PDF
  - 🔑 Generate Key Points
  - 📖 Generate Glossary

### 5. View History
- Check sidebar for chat history
- Click "Clear Chat" to reset

**See `USAGE_GUIDE.md` for detailed usage instructions.**

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USER/REPO.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository
   - Set main file: `app.py`
   - Add secret: `GOOGLE_API_KEY`

3. **Done!** App is live at `https://YOUR_APP.streamlit.app`

**See `DEPLOYMENT.md` for detailed deployment guide.**

---

## 🔧 Configuration

### Chunking Parameters
```python
# In utils/helpers.py
chunk_size=600      # Target tokens (500-800 range)
overlap=100         # Overlap tokens
```

### Retrieval Parameters
```python
# In core/retrieval.py
top_k=5             # Number of results
min_relevance=0.3   # Minimum relevance (0-1)
```

### Streaming
```python
# Toggle in sidebar UI
streaming_enabled=True
```

---

## 📊 Performance

### Processing Times
| Document Size | Time |
|--------------|------|
| 5 pages | 30-60 seconds |
| 20 pages | 60-120 seconds |
| 50 pages | 120-180 seconds |

### Response Times
| Operation | Time |
|-----------|------|
| Single question | 5-15 seconds |
| Streaming response | 5-20 seconds |
| Complex query | 15-30 seconds |

### Memory Usage
| PDF Size | Memory |
|----------|--------|
| Small (5-10 pages) | ~200 MB |
| Medium (20-50 pages) | ~400 MB |
| Large (50+ pages) | ~600 MB |

---

## 🎓 Features in Detail

### Multi-PDF Support
- Upload multiple PDFs at once
- Unified knowledge base
- Query across all documents
- Source tracking with PDF name + page

### Advanced Text Processing
- **pdfplumber**: High-quality extraction
- **OCR**: Scanned PDF support (pytesseract)
- **Tables**: Extract and query tables
- **Images**: Extract for vision Q&A

### Vector Database
- **FAISS CPU**: Fast similarity search
- **Gemini Embeddings**: `models/embedding-001`
- **Chunking**: 500-800 tokens per chunk
- **Relevance Scores**: 0-100% similarity

### Citations
- Page numbers
- PDF names
- Highlighted snippets
- Relevance scores
- Expandable references

### Summarization
- Full PDF summary
- Key points extraction
- Glossary generation
- Page-specific summaries

### Streaming
- Real-time token generation
- ChatGPT-like experience
- Toggle on/off
- Graceful fallback

**See `ENHANCED_FEATURES.md` for complete feature documentation.**

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**"API key not found"**
- Check `.env` file exists
- Verify format: `GOOGLE_API_KEY=your_key`
- Restart app after changes

**"OCR not working"**
- Install Tesseract: `sudo apt-get install tesseract-ocr`
- Install packages: `pip install pytesseract pdf2image`

**"FAISS error"**
```bash
pip install faiss-cpu
# Note: Use faiss-cpu, not faiss
```

**"Port 8501 in use"**
```bash
streamlit run app.py --server.port 8502
```

**See `INSTALLATION.md` for more troubleshooting.**

---

## 📚 Documentation

- **README.md** - Main documentation (this file)
- **INSTALLATION.md** - Detailed installation guide
- **ENHANCED_FEATURES.md** - Complete feature documentation
- **UPGRADE_GUIDE.md** - Upgrade from basic version
- **USAGE_GUIDE.md** - User guide with examples
- **DEPLOYMENT.md** - Deployment instructions
- **TESTING.md** - Testing procedures

---

## 🔒 Security

- API keys stored in `.env` (not in repo)
- `.env` in `.gitignore`
- Streamlit Cloud secrets for production
- No sensitive data in code

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Powerful language model
- **Streamlit** - Amazing web framework
- **FAISS** - Efficient vector search
- **Open Source Community** - Inspiration and tools

---

## 🆘 Support

- **Issues**: Open a GitHub issue
- **Documentation**: Check docs in project
- **Questions**: Review troubleshooting sections
- **Streamlit**: https://docs.streamlit.io
- **Gemini**: https://ai.google.dev/docs

---

## 🎉 What's New in Enhanced Version

### Compared to Basic Version

✅ **Multi-PDF** - Query across multiple documents
✅ **OCR** - Process scanned PDFs
✅ **Tables** - Extract and query tables
✅ **Images** - Vision Q&A ready
✅ **Better Chunking** - 500-800 token chunks
✅ **Relevance Scores** - Source ranking
✅ **Streaming** - Real-time responses
✅ **Summarization** - 4 summary types
✅ **Enhanced UI** - Statistics, history, controls
✅ **Better Architecture** - Modular code

**See `UPGRADE_GUIDE.md` for migration instructions.**

---

## 📈 Roadmap

Future enhancements:
- [ ] Custom chunk size in UI
- [ ] Model selection dropdown
- [ ] Export chat history
- [ ] Multi-language support
- [ ] Advanced filtering
- [ ] Batch processing
- [ ] Cloud storage integration

---

**Made with ❤️ using Python, Streamlit, and Google Gemini AI**

**Ready for production use!** 🚀

