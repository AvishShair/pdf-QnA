# 🧪 Testing Guide

Guide for testing the PDF Q&A Bot locally before deployment.

## 🎯 Pre-Testing Checklist

Before you begin testing, ensure:

- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid API key
- [ ] API key is valid and has quota available
- [ ] Internet connection is stable

## 🚀 Running Tests

### 1. Environment Test

**Test**: Verify environment setup

```bash
# Check Python version
python --version  # Should be 3.10 or higher

# Check if dependencies are installed
pip list | grep streamlit
pip list | grep google-generativeai
pip list | grep faiss-cpu

# Verify .env file exists
cat .env  # Should show GOOGLE_API_KEY=...
```

**Expected Result**: All commands run without errors

### 2. Application Launch Test

**Test**: Launch the application

```bash
streamlit run app.py
```

**Expected Results**:
- ✅ App starts without errors
- ✅ Browser opens automatically to `http://localhost:8501`
- ✅ UI loads completely
- ✅ No error messages in terminal
- ✅ Sidebar is visible
- ✅ Main area shows welcome message

**Common Issues**:
- Port 8501 in use → Kill process or use `streamlit run app.py --server.port 8502`
- Module not found → Install missing dependency
- API key error → Check `.env` file

### 3. API Key Test

**Test**: Verify API key is loaded

**Steps**:
1. Launch app
2. Check sidebar
3. Look for "✅ API Key loaded" message

**Expected Results**:
- ✅ Green checkmark with "API Key loaded"
- ❌ If warning appears, check `.env` file

**Manual Entry Test**:
1. Rename `.env` to `.env.backup`
2. Restart app
3. Enter API key in sidebar text box
4. Should see success message

### 4. PDF Upload Test

**Test**: Upload a PDF file

**Test PDFs**: Use any of these:
- Sample research paper (5-10 pages)
- Company report (10-20 pages)
- Technical documentation (any length)
- [Download test PDF](https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf)

**Steps**:
1. Click "Browse files" in sidebar
2. Select a test PDF
3. Verify file appears in uploader
4. Check file name is displayed

**Expected Results**:
- ✅ File uploads successfully
- ✅ File name appears
- ✅ Process button is clickable
- ✅ No error messages

**Multiple PDF Test**:
1. Upload 2-3 PDFs at once
2. Verify all appear in list

### 5. PDF Processing Test

**Test**: Process uploaded PDF

**Steps**:
1. Upload a test PDF
2. Click "🚀 Process PDFs"
3. Watch progress messages
4. Wait for completion

**Expected Results**:
- ✅ "📄 Extracting text from PDFs..." appears
- ✅ "🔪 Chunking text..." appears
- ✅ "📊 Created X text chunks" message
- ✅ "🧠 Creating embeddings..." appears
- ✅ "✅ Vector store created" success message
- ✅ "🤖 Initializing QA Engine..." appears
- ✅ "✅ QA Engine ready!" appears
- ✅ Uploaded files list appears in sidebar
- ✅ Chat input becomes active

**Performance Benchmarks**:
- 5-page PDF: ~30-60 seconds
- 20-page PDF: ~60-120 seconds
- 50-page PDF: ~120-180 seconds

**Error Scenarios to Test**:
1. **Corrupted PDF**: Should show error message
2. **Empty PDF**: Should handle gracefully
3. **Very large PDF** (100+ pages): Should work but take longer
4. **Password-protected PDF**: Should show error

### 6. Question-Answer Test

**Test**: Ask questions and verify answers

**Test Cases**:

#### Test Case 1: Basic Question
```
Upload: Any document
Question: "What is this document about?"
Expected: Summary of the document's main topic
```

#### Test Case 2: Specific Information
```
Upload: Research paper
Question: "Who are the authors?"
Expected: List of authors or indication if not found
```

#### Test Case 3: Detail Extraction
```
Upload: Technical manual
Question: "What are the system requirements?"
Expected: Specific requirements listed in document
```

#### Test Case 4: No Information
```
Upload: Any document
Question: "What is the weather in Tokyo?"
Expected: "I couldn't find relevant information..."
```

#### Test Case 5: Follow-up Questions
```
Question 1: "What is the main topic?"
Question 2: "Can you elaborate on that?"
Expected: Bot uses context from previous answer
```

**Expected Results for All Questions**:
- ✅ Response appears within 10-30 seconds
- ✅ Answer is relevant to question
- ✅ Sources section appears (expandable)
- ✅ Message appears in chat history
- ✅ No error messages

### 7. Sources Citation Test

**Test**: Verify source citations

**Steps**:
1. Ask any question
2. Wait for answer
3. Click "📚 View Sources" expander
4. Check source information

**Expected Results**:
- ✅ Sources section expandable
- ✅ Shows 1-3 source chunks
- ✅ Each source shows:
  - Source ID (1, 2, 3)
  - Filename
  - Chunk ID
  - Relevance percentage
  - Text excerpt
- ✅ Text is readable and relevant

### 8. Chat History Test

**Test**: Verify chat history functionality

**Steps**:
1. Ask 3-5 different questions
2. Scroll up to see history
3. Verify all messages are visible
4. Click "🗑️ Clear Chat History"
5. Verify history is cleared

**Expected Results**:
- ✅ All messages appear in order
- ✅ User messages in blue boxes
- ✅ Bot messages in gray boxes
- ✅ Clear button works
- ✅ History resets after clearing

### 9. Error Handling Test

**Test**: Verify error handling

**Error Scenarios**:

#### Invalid API Key
```
Steps:
1. Set wrong API key in .env
2. Restart app
3. Try to process PDF
Expected: Clear error message about API key
```

#### Network Failure
```
Steps:
1. Disconnect internet
2. Try to ask question
Expected: Network error message
```

#### Invalid PDF
```
Steps:
1. Try to upload non-PDF file
Expected: File type error or prevented upload
```

#### Empty Question
```
Steps:
1. Submit empty question
Expected: Nothing happens or prompt for input
```

### 10. UI/UX Test

**Test**: Verify user interface quality

**Checklist**:
- [ ] Title displays correctly
- [ ] Colors are pleasing and readable
- [ ] Buttons are clickable
- [ ] Text is readable (not too small/large)
- [ ] Sidebar is functional
- [ ] No layout issues
- [ ] Responsive design (resize window)
- [ ] Instructions are clear
- [ ] Error messages are visible
- [ ] Success messages are clear

### 11. Performance Test

**Test**: Verify performance under load

**Test Cases**:

1. **Large PDF** (50+ pages)
   - Upload and process
   - Should complete without crash
   - May take 2-5 minutes

2. **Multiple PDFs** (5 PDFs)
   - Upload 5 documents
   - Process together
   - Verify all are processed

3. **Many Questions** (20+ questions)
   - Ask 20 questions in a row
   - Verify all are answered
   - Check memory usage

4. **Long Chat Session**
   - Keep app running for 30 minutes
   - Ask questions periodically
   - Verify no degradation

### 12. Integration Test

**Test**: End-to-end workflow

**Complete Workflow**:
```
1. Launch app → Success
2. Verify API key → Loaded
3. Upload 2 PDFs → Uploaded
4. Process PDFs → Completed
5. Ask question 1 → Answered with sources
6. Ask question 2 → Answered with sources
7. Ask follow-up → Uses context correctly
8. Check sources → All visible and relevant
9. Clear history → Cleared
10. Ask new question → Answered
11. Close app → No errors
```

**Expected**: All steps complete successfully

## 📊 Test Results Template

Use this template to record test results:

```
Date: ___________
Tester: ___________
Environment: Local / Streamlit Cloud

| Test Name              | Status | Notes |
|------------------------|--------|-------|
| Environment Setup      | ✅ / ❌ |       |
| App Launch             | ✅ / ❌ |       |
| API Key Loading        | ✅ / ❌ |       |
| PDF Upload             | ✅ / ❌ |       |
| PDF Processing         | ✅ / ❌ |       |
| Question-Answer        | ✅ / ❌ |       |
| Source Citations       | ✅ / ❌ |       |
| Chat History           | ✅ / ❌ |       |
| Error Handling         | ✅ / ❌ |       |
| UI/UX Quality          | ✅ / ❌ |       |
| Performance            | ✅ / ❌ |       |
| End-to-end Workflow    | ✅ / ❌ |       |

Overall Status: ✅ PASS / ❌ FAIL

Issues Found:
1. ___________
2. ___________

Recommendations:
1. ___________
2. ___________
```

## 🔧 Debugging Tips

### Check Logs

**Terminal Output**:
```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug
```

**Look for**:
- `INFO` messages: Normal operation
- `WARNING` messages: Potential issues
- `ERROR` messages: Failures

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "API key not found" | Missing or invalid key | Check `.env` file |
| "Failed to extract text" | Corrupted PDF | Try different PDF |
| "Connection error" | Network issue | Check internet |
| "Rate limit exceeded" | Too many requests | Wait and retry |
| "FAISS error" | Installation issue | Reinstall faiss-cpu |

### Browser Developer Tools

1. Press F12 to open DevTools
2. Check Console for JavaScript errors
3. Check Network tab for API failures
4. Check Application tab for storage issues

## ✅ Pre-Deployment Checklist

Before deploying to production:

- [ ] All tests pass
- [ ] No errors in logs
- [ ] Performance is acceptable
- [ ] UI looks good
- [ ] Error messages are user-friendly
- [ ] API key is secured
- [ ] Documentation is complete
- [ ] `.gitignore` excludes `.env`
- [ ] `requirements.txt` is up to date
- [ ] Code is clean and commented

## 🎓 Testing Best Practices

1. **Test with Real Data**
   - Use actual PDFs you plan to query
   - Test with various document types

2. **Test Edge Cases**
   - Very small PDFs (1 page)
   - Very large PDFs (100+ pages)
   - PDFs with images/tables
   - PDFs with special characters

3. **Test Error Scenarios**
   - Always test what happens when things go wrong
   - Verify user gets helpful error messages

4. **Document Issues**
   - Keep track of bugs found
   - Note steps to reproduce
   - Prioritize fixes

5. **Retest After Changes**
   - After fixing bugs, retest
   - Verify fix doesn't break other features

## 🐛 Reporting Issues

When reporting issues, include:

1. **Description**: What went wrong?
2. **Steps to Reproduce**: How to trigger the error?
3. **Expected**: What should happen?
4. **Actual**: What actually happened?
5. **Environment**: OS, Python version, etc.
6. **Logs**: Error messages or stack traces
7. **Screenshots**: If UI issue

## 📞 Support

If you encounter issues during testing:

1. Check the troubleshooting section in README.md
2. Review error logs carefully
3. Search for similar issues online
4. Open a GitHub issue with details

---

**Happy Testing! 🧪✨**

