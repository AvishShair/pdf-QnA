# 📦 Installation Guide

Complete installation guide for the Enhanced PDF Q&A Bot.

## 🎯 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Optional (for OCR)
- Tesseract OCR (for scanned PDF processing)
- System dependencies for image processing

## 🚀 Quick Installation

### Step 1: Clone/Download Project
```bash
cd "/home/test/Desktop/pdfq&a"
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key
Create `.env` file:
```bash
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

Or manually create `.env`:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 5: Run Application
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

## 📋 Detailed Installation

### Python Setup

#### Check Python Version
```bash
python --version  # Should be 3.10+
```

#### Install Python (if needed)
- **Ubuntu/Debian**: `sudo apt-get install python3.10 python3-pip`
- **macOS**: `brew install python@3.10`
- **Windows**: Download from [python.org](https://www.python.org)

### Dependencies Installation

#### Core Dependencies
```bash
pip install streamlit==1.31.0
pip install google-generativeai==0.3.2
pip install python-dotenv==1.0.0
pip install PyPDF2==3.0.1
pip install pdfplumber==0.10.3
pip install faiss-cpu==1.7.4
pip install numpy==1.24.3
pip install tiktoken==0.5.1
```

#### OCR Dependencies (Optional)
```bash
pip install pytesseract==0.3.10
pip install pdf2image==1.16.3
pip install Pillow==10.1.0
```

#### System Dependencies for OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install tesseract
brew install poppler
```

**Windows:**
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases

### Verify Installation

```bash
# Check Python
python --version

# Check packages
pip list | grep streamlit
pip list | grep google-generativeai
pip list | grep faiss

# Test imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import google.generativeai; print('Gemini OK')"
python -c "import faiss; print('FAISS OK')"
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:
```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional (for OCR)
TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
```

### Get API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env` file

## 🧪 Testing Installation

### Test 1: Basic Import
```bash
python -c "from core.pdf_parser import EnhancedPDFParser; print('OK')"
```

### Test 2: Run App
```bash
streamlit run app.py
```

Should see:
- ✅ App launches
- ✅ No import errors
- ✅ UI loads

### Test 3: Process PDF
1. Upload a test PDF
2. Click "Process PDFs"
3. Should complete without errors

## 🐛 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
# Or reinstall all:
pip install -r requirements.txt
```

### Issue: "FAISS not found"
**Solution:**
```bash
pip install faiss-cpu
# Note: Use faiss-cpu, not faiss (for Streamlit Cloud compatibility)
```

### Issue: "OCR not working"
**Solution:**
1. Install Tesseract on system (see above)
2. Install Python packages:
   ```bash
   pip install pytesseract pdf2image
   ```
3. Verify Tesseract:
   ```bash
   tesseract --version
   ```

### Issue: "API key error"
**Solution:**
1. Check `.env` file exists
2. Verify key format: `GOOGLE_API_KEY=your_key`
3. No quotes around key
4. Restart app after changing `.env`

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9
```

### Issue: "Memory error"
**Solution:**
- Use smaller PDFs
- Reduce chunk size in code
- Close other applications
- Increase system memory

## 📊 System Requirements

### Minimum
- **RAM**: 2 GB
- **Storage**: 500 MB
- **CPU**: 2 cores
- **Python**: 3.10+

### Recommended
- **RAM**: 4 GB+
- **Storage**: 1 GB+
- **CPU**: 4 cores+
- **Python**: 3.11+

### For Large PDFs
- **RAM**: 8 GB+
- **Storage**: 2 GB+
- **CPU**: 8 cores+

## 🌐 Cloud Deployment

### Streamlit Cloud
See `DEPLOYMENT.md` for detailed instructions.

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## ✅ Installation Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created
- [ ] API key configured
- [ ] App launches successfully
- [ ] PDF upload works
- [ ] Processing completes
- [ ] Questions get answered

## 🆘 Getting Help

If installation fails:
1. Check error messages
2. Verify Python version
3. Check dependencies
4. Review troubleshooting section
5. Check logs for details

## 📚 Next Steps

After installation:
1. Read `README.md` for usage
2. Read `ENHANCED_FEATURES.md` for features
3. Read `USAGE_GUIDE.md` for tips
4. Try uploading a PDF
5. Ask your first question!

---

**Installation complete! Ready to use!** 🎉

