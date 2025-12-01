# 🔄 Upgrade Guide: Enhanced PDF Q&A Bot

This guide explains how to upgrade from the basic version to the enhanced version with all new features.

## 📋 What's New

### Major Enhancements
1. ✅ **Multi-PDF Support** - Unified knowledge base
2. ✅ **OCR Support** - Scanned PDF processing
3. ✅ **Table Extraction** - Extract and query tables
4. ✅ **Image Extraction** - Vision-based Q&A ready
5. ✅ **Enhanced Chunking** - 500-800 token chunks
6. ✅ **Relevance Scores** - Better source ranking
7. ✅ **Streaming Responses** - Real-time token streaming
8. ✅ **Summarization Tools** - 4 types of summaries
9. ✅ **Enhanced UI** - Better statistics and controls
10. ✅ **Improved Architecture** - Modular code structure

## 🚀 Migration Steps

### Step 1: Backup Existing Code
```bash
cd "/home/test/Desktop/pdfq&a"
cp -r . ../pdfq&a_backup
```

### Step 2: Update Dependencies
```bash
# Install new dependencies
pip install -r requirements.txt --upgrade

# New dependencies:
# - pytesseract (for OCR)
# - pdf2image (for image extraction)
# - tiktoken (for token counting)
```

### Step 3: Update Code Structure
The new structure uses `core/`, `ui/`, and `utils/` directories:
```
pdfq&a/
├── app.py              # Updated main app
├── core/               # NEW: Core modules
│   ├── pdf_parser.py
│   ├── ocr.py
│   ├── embedder.py
│   ├── retrieval.py
│   └── qa_engine.py
├── ui/                 # NEW: UI components
│   └── components.py
└── utils/              # NEW: Utilities
    └── helpers.py
```

### Step 4: Update Environment Variables
No changes needed - same `.env` file format:
```
GOOGLE_API_KEY=your_api_key
```

### Step 5: Test the Upgrade
```bash
streamlit run app.py
```

## 🔧 Configuration Changes

### New Processing Options
In the sidebar, you'll see new checkboxes:
- ✅ Use OCR (for scanned PDFs)
- ✅ Extract Tables
- ✅ Extract Images

### New UI Elements
- Statistics panel (PDFs, pages, chunks)
- History panel (last 10 messages)
- Streaming toggle
- Summarization buttons

## 📝 Code Changes

### Import Changes
**Old:**
```python
from utils.pdf_parser import PDFParser
from utils.embedder import TextEmbedder
from utils.qa_engine import QAEngine
```

**New:**
```python
from core.pdf_parser import EnhancedPDFParser
from core.embedder import EnhancedEmbedder
from core.retrieval import RetrievalEngine
from core.qa_engine import EnhancedQAEngine
```

### Processing Changes
**Old:**
```python
parser = PDFParser()
results = parser.extract_from_multiple_pdfs(files)
```

**New:**
```python
parser = EnhancedPDFParser()
results = parser.extract_from_multiple_pdfs(
    files,
    use_ocr=True,      # NEW
    extract_tables=True,  # NEW
    extract_images=False  # NEW
)
```

### Chunking Changes
**Old:**
```python
chunks = chunk_text(text, chunk_size=1000, overlap=200)
```

**New:**
```python
chunks = chunk_text_by_tokens(
    text,
    chunk_size=600,  # 500-800 range
    overlap=100
)
```

## 🐛 Troubleshooting

### Issue: "Module not found: core"
**Solution**: Ensure you're in the project root directory

### Issue: "OCR not working"
**Solution**: 
1. Install Tesseract: `sudo apt-get install tesseract-ocr`
2. Install Python packages: `pip install pytesseract pdf2image`

### Issue: "Streaming not working"
**Solution**: 
- Check API key is valid
- Ensure Gemini API supports streaming
- Try disabling streaming toggle

### Issue: "Chunking errors"
**Solution**: 
- Check tiktoken is installed: `pip install tiktoken`
- Verify text extraction worked

## ✅ Verification Checklist

After upgrade, verify:
- [ ] App launches without errors
- [ ] PDF upload works
- [ ] Processing completes
- [ ] Questions get answered
- [ ] Sources show page numbers
- [ ] Streaming works (if enabled)
- [ ] Summarization buttons work
- [ ] Statistics panel shows data
- [ ] History panel displays messages

## 📚 Additional Resources

- See `ENHANCED_FEATURES.md` for feature details
- See `README.md` for general usage
- See `DEPLOYMENT.md` for deployment

## 🆘 Need Help?

If you encounter issues:
1. Check error messages in terminal
2. Review logs for details
3. Verify all dependencies installed
4. Check API key is valid
5. Review troubleshooting section

---

**Upgrade complete! Enjoy the enhanced features!** 🎉

