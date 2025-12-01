# ⚡ Quick Start Guide

Get your PDF Q&A Bot running in 5 minutes!

---

## 🚀 Local Setup (5 Steps)

### Step 1: Get API Key (2 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Install Dependencies (1 minute)

```bash
cd "/home/test/Desktop/pdfq&a"
pip install -r requirements.txt
```

### Step 3: Configure API Key (30 seconds)

Create a `.env` file:

```bash
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

Or create `.env` manually and add:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 4: Run the App (30 seconds)

```bash
streamlit run app.py
```

### Step 5: Use the App (1 minute)

1. Browser opens automatically at http://localhost:8501
2. Upload a PDF using the sidebar
3. Click "Process PDFs"
4. Ask questions in the chat box!

---

## 🌐 Streamlit Cloud Deployment (5 Steps)

### Step 1: Push to GitHub

```bash
cd "/home/test/Desktop/pdfq&a"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Go to Streamlit Cloud

Visit: https://share.streamlit.io

### Step 3: Deploy

1. Click "New app"
2. Select your repository
3. Set main file: `app.py`
4. Click "Advanced settings"

### Step 4: Add Secret

In the Secrets section, add:
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### Step 5: Deploy!

Click "Deploy" and wait 2-5 minutes.

Your app will be live at: `https://YOUR_APP.streamlit.app`

---

## 💡 First Test

1. **Upload**: Use any PDF (research paper, report, manual)
2. **Process**: Click "Process PDFs" button
3. **Ask**: Type "What is this document about?"
4. **View**: See answer and sources!

---

## 📚 Example Questions

- "What are the main findings?"
- "Summarize the key points"
- "Who are the authors?"
- "What methodology was used?"
- "What are the conclusions?"

---

## ❓ Common Issues

### "No module named 'streamlit'"
**Fix**: Run `pip install -r requirements.txt`

### "API key not found"
**Fix**: Create `.env` file with your API key

### "Failed to extract text"
**Fix**: Ensure PDF is text-based (not image-only)

### Port 8501 already in use
**Fix**: Run `streamlit run app.py --server.port 8502`

---

## 📖 Need More Help?

- **Full Documentation**: See README.md
- **Deployment Guide**: See DEPLOYMENT.md
- **Usage Tips**: See USAGE_GUIDE.md
- **Testing**: See TESTING.md

---

## ✅ Success Checklist

- [ ] API key obtained
- [ ] Dependencies installed
- [ ] `.env` file created
- [ ] App launches without errors
- [ ] PDF uploads successfully
- [ ] Processing completes
- [ ] Questions get answered
- [ ] Sources are shown

---

**That's it! You're ready to query your PDFs with AI! 🎉**

