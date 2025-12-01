# 📄 PDF Question Answering Bot

A production-ready PDF Question-Answer Bot powered by **Google Gemini AI** and **Streamlit**. Upload your PDF documents and ask questions to get intelligent answers with source citations.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 📤 **Multi-PDF Upload**: Upload and process multiple PDF documents simultaneously
- 🧠 **AI-Powered Q&A**: Leverages Google's Gemini 1.5 Flash model for intelligent answers
- 🔍 **Semantic Search**: Uses FAISS vector store for efficient similarity search
- 📚 **Source Citations**: Shows the exact text chunks used to generate answers
- 💬 **Chat History**: Maintains conversation context for better responses
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface
- ⚡ **Production Ready**: Error handling, logging, and modular architecture

## 🏗️ Project Structure

```
pdfq&a/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── utils/
│   ├── __init__.py           # Utils package
│   ├── pdf_parser.py         # PDF text extraction
│   ├── embedder.py           # FAISS vector store & embeddings
│   └── qa_engine.py          # Question answering engine
└── .streamlit/
    └── config.toml           # Streamlit configuration (optional)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Installation

1. **Clone or download this repository**

```bash
cd /path/to/pdfq&a
```

2. **Create a virtual environment**

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

Or edit `.env` manually:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

5. **Run the application**

```bash
streamlit run app.py
```

6. **Open in browser**

The app will automatically open at `http://localhost:8501`

## 📖 How to Use

1. **Start the app** using the command above
2. **Enter your API key** (if not in `.env` file)
3. **Upload PDF files** using the sidebar file uploader
4. **Click "Process PDFs"** to extract and index the content
5. **Ask questions** in the chat input box
6. **View answers** with source citations
7. **Continue the conversation** - the bot remembers context
8. **Clear chat** anytime using the "Clear Chat History" button

## 🌐 Deploy to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**

```bash
git init
git add .
git commit -m "Initial commit: PDF Q&A Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Ensure `.gitignore` excludes sensitive files**

The `.gitignore` file already excludes `.env` and other sensitive files.

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Advanced settings"
7. Add your API key as a secret:
   ```
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
8. Click "Deploy"!

### Step 3: Configure Secrets (Important!)

In Streamlit Cloud, go to **App settings** → **Secrets** and add:

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | Yes |

### Customization

You can customize various parameters in the code:

**PDF Parser** (`utils/pdf_parser.py`):
- `chunk_size`: Size of text chunks (default: 1000)
- `overlap`: Overlap between chunks (default: 200)

**QA Engine** (`utils/qa_engine.py`):
- `model_name`: Gemini model (default: "gemini-1.5-flash")
- `temperature`: Response randomness (default: 0.7)
- `max_output_tokens`: Maximum response length (default: 2048)

**Embedder** (`utils/embedder.py`):
- `top_k`: Number of relevant chunks to retrieve (default: 3)

## 📦 Dependencies

- **streamlit**: Web application framework
- **google-generativeai**: Google Gemini API client
- **PyPDF2**: PDF text extraction
- **pdfplumber**: Alternative PDF parser (fallback)
- **faiss-cpu**: Vector similarity search
- **python-dotenv**: Environment variable management
- **langchain**: Text processing utilities

## 🐛 Troubleshooting

### Issue: "No module named 'faiss'"

**Solution**: FAISS is automatically installed. If issues persist:
```bash
pip install faiss-cpu --no-cache-dir
```

### Issue: "API key not found"

**Solution**: Ensure your `.env` file exists and contains:
```
GOOGLE_API_KEY=your_actual_key
```

Or enter it directly in the Streamlit sidebar.

### Issue: "Failed to extract text from PDF"

**Solution**: 
- Try a different PDF file
- The app uses both PyPDF2 and pdfplumber as fallback
- Some PDFs may be image-based (not supported yet)

### Issue: "Rate limit exceeded"

**Solution**: 
- Wait a few moments between requests
- Check your Gemini API quota
- Consider upgrading your API plan

## 🔒 Security Notes

- **Never commit `.env` files** to version control
- **Use Streamlit Cloud secrets** for production deployments
- **Rotate API keys** regularly
- **Monitor API usage** in Google Cloud Console

## 🎯 Future Enhancements

- [ ] Support for image-based PDFs (OCR)
- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Advanced filtering and search options
- [ ] Export chat history
- [ ] Multi-language support
- [ ] Custom model selection in UI
- [ ] Batch question processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for the powerful language model
- Streamlit for the amazing web framework
- FAISS for efficient vector search
- The open-source community

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Review Gemini API documentation: [ai.google.dev](https://ai.google.dev)

---

**Made with ❤️ using Python, Streamlit, and Google Gemini AI**

