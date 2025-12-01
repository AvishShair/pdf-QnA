# 📖 Usage Guide

Complete guide on how to use the PDF Question-Answer Bot effectively.

## 🎯 Getting Started

### Initial Setup

1. **Launch the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API Key**
   - Option A: Set in `.env` file (recommended)
   - Option B: Enter in sidebar when app starts

3. **Verify Setup**
   - You should see "✅ API Key loaded" in the sidebar

## 📤 Uploading PDFs

### Supported Formats

- ✅ Standard PDF files (.pdf)
- ✅ Multi-page documents
- ✅ Text-based PDFs
- ❌ Image-only PDFs (not supported yet)
- ❌ Password-protected PDFs

### How to Upload

1. **Single PDF**
   - Click "Browse files" in sidebar
   - Select your PDF file
   - Click "Open"

2. **Multiple PDFs**
   - Click "Browse files"
   - Hold Ctrl (Windows/Linux) or Cmd (Mac)
   - Select multiple PDF files
   - Click "Open"

3. **Process PDFs**
   - After uploading, click "🚀 Process PDFs"
   - Wait for processing to complete
   - Look for success messages

### What Happens During Processing

1. **Text Extraction** (10-30 seconds)
   - Extracts text from all pages
   - Uses PyPDF2 with pdfplumber fallback
   - Handles extraction errors gracefully

2. **Text Chunking** (5-10 seconds)
   - Splits text into manageable chunks
   - Default: 1000 characters per chunk
   - 200 character overlap for context

3. **Embedding Creation** (30-60 seconds)
   - Creates vector embeddings for each chunk
   - Uses Google's embedding model
   - Stores in FAISS vector database

4. **QA Engine Initialization** (5 seconds)
   - Sets up Gemini AI model
   - Tests API connection
   - Prepares for questions

## 💬 Asking Questions

### Best Practices

✅ **Good Questions:**
- "What are the main findings of this research?"
- "Summarize the key points from section 3"
- "What is the definition of [term] in this document?"
- "How does the author describe [concept]?"
- "What are the recommendations mentioned?"

❌ **Less Effective Questions:**
- Single words: "Introduction"
- Too vague: "Tell me about this"
- Unrelated: "What's the weather?"

### Question Types

#### 1. **Factual Questions**
```
Q: What is the publication date of this paper?
Q: Who are the authors mentioned?
Q: What are the three main conclusions?
```

#### 2. **Explanatory Questions**
```
Q: How does the proposed algorithm work?
Q: Explain the methodology used in this study
Q: What is the relationship between X and Y?
```

#### 3. **Summary Questions**
```
Q: Summarize the abstract
Q: What are the key takeaways from this document?
Q: Give me an overview of chapter 2
```

#### 4. **Comparative Questions**
```
Q: What are the differences between approach A and B?
Q: How do the results compare to previous studies?
Q: What are the pros and cons mentioned?
```

#### 5. **Analytical Questions**
```
Q: What are the limitations of this study?
Q: What gaps does the author identify?
Q: What future research is suggested?
```

## 📚 Understanding Responses

### Response Components

Each answer includes:

1. **Main Answer**
   - AI-generated response
   - Based on retrieved context
   - Clear and concise

2. **Sources Section** (expandable)
   - Text chunks used
   - Source document name
   - Chunk ID and relevance score

### Interpreting Relevance Scores

- **90-100%**: Highly relevant
- **70-89%**: Moderately relevant
- **50-69%**: Somewhat relevant
- **<50%**: May not be directly relevant

### When No Answer is Found

If the bot says "I couldn't find relevant information":
- The information may not be in the uploaded PDFs
- Try rephrasing your question
- Use different keywords
- Upload additional documents

## 🔄 Chat History

### Using Conversation Context

The bot remembers previous messages:

```
You: What is the main topic of this paper?
Bot: The paper discusses machine learning applications...

You: What methodology did they use?
Bot: [Uses context from previous answer]

You: What were the results?
Bot: [Continues the conversation naturally]
```

### Clearing History

Click "🗑️ Clear Chat History" to:
- Start a fresh conversation
- Remove context from previous questions
- Free up memory

## 🎨 UI Features

### Sidebar Components

1. **Configuration**
   - API key status
   - Model information

2. **Upload Section**
   - File uploader
   - Process button

3. **Document List**
   - Shows loaded PDFs
   - Number of documents

4. **Controls**
   - Clear chat button
   - Settings (if applicable)

5. **Instructions**
   - Quick how-to guide
   - Links to documentation

### Main Chat Area

1. **Conversation View**
   - User messages (blue)
   - Bot responses (gray)
   - Source citations

2. **Input Box**
   - Type questions here
   - Press Enter to send

## 💡 Tips and Tricks

### For Better Results

1. **Be Specific**
   - ✅ "What are the three main advantages mentioned in section 2?"
   - ❌ "Tell me about advantages"

2. **Use Context**
   - Reference specific sections, chapters, or pages
   - Use terms from the document

3. **Break Down Complex Questions**
   - Instead of: "Explain everything about the methodology and results"
   - Try: 
     1. "What methodology was used?"
     2. "What were the results?"
     3. "How do the results support the hypothesis?"

4. **Ask Follow-up Questions**
   - The bot remembers context
   - Build on previous answers

5. **Check Sources**
   - Expand the sources section
   - Verify the information
   - Read full context if needed

### Performance Optimization

1. **PDF Size**
   - Smaller PDFs process faster
   - Consider splitting very large documents

2. **Number of PDFs**
   - More PDFs = longer processing time
   - Balance comprehensiveness vs. speed

3. **Question Complexity**
   - Simple questions get faster responses
   - Complex questions may take longer

## 🔍 Advanced Features

### Multiple Document Queries

Ask questions across multiple documents:
```
Q: Compare the findings from all the uploaded papers
Q: What common themes appear in these documents?
Q: Which document discusses [topic] in most detail?
```

### Citation Analysis

Use the source view to:
- Verify information accuracy
- Find exact page/section
- Read surrounding context
- Identify source document

## 🐛 Common Issues and Solutions

### Issue: Slow Processing

**Solutions:**
- Wait patiently (first time is slower)
- Check internet connection
- Try smaller PDFs
- Reduce number of documents

### Issue: Irrelevant Answers

**Solutions:**
- Rephrase your question
- Be more specific
- Check if topic is in the PDFs
- Upload more relevant documents

### Issue: "No relevant information found"

**Solutions:**
- Topic may not be in documents
- Try different keywords
- Check document upload was successful
- Verify PDF text extraction worked

### Issue: API Errors

**Solutions:**
- Check API key is correct
- Verify internet connection
- Check API quota/limits
- Wait and retry

## 📊 Example Workflow

### Research Paper Analysis

1. Upload research paper PDF
2. Click "Process PDFs"
3. Start with broad question: "What is this paper about?"
4. Ask specific questions:
   - "What methodology was used?"
   - "What are the main findings?"
   - "What are the limitations?"
   - "What future work is suggested?"
5. Review sources for details

### Legal Document Review

1. Upload contract or legal document
2. Process the document
3. Ask targeted questions:
   - "What are the key terms and conditions?"
   - "What are the parties' obligations?"
   - "What is the termination clause?"
   - "What are the penalties mentioned?"
4. Verify with source citations

### Technical Manual Query

1. Upload technical documentation
2. Process the files
3. Ask how-to questions:
   - "How do I configure authentication?"
   - "What are the system requirements?"
   - "How do I troubleshoot error X?"
4. Follow step-by-step from answers

## 🎓 Learning Resources

### Improve Your Questions

- Be clear and specific
- Use proper terminology
- Reference context when available
- Ask one thing at a time

### Understand AI Limitations

- AI generates based on context only
- Cannot access external information
- May occasionally misinterpret
- Always verify critical information

### Best Use Cases

✅ **Excellent for:**
- Quick information retrieval
- Document summarization
- Finding specific details
- Comparing information
- Understanding concepts

⚠️ **Less suitable for:**
- Legal advice (consult professional)
- Medical decisions (consult doctor)
- Financial recommendations
- Image/chart interpretation

## 🆘 Getting Help

If you need assistance:

1. Check this usage guide
2. Review the README.md
3. Check troubleshooting section
4. Review error messages
5. Contact support or open an issue

---

**Happy querying! 📚✨**

