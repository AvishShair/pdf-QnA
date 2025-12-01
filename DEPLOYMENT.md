# 🚀 Deployment Guide

This guide covers how to deploy the PDF Q&A Bot to Streamlit Cloud.

## 📋 Prerequisites

- GitHub account
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Your code pushed to a GitHub repository

## 🌐 Deploy to Streamlit Cloud

### Step 1: Prepare Your GitHub Repository

1. **Create a new repository on GitHub**
   - Go to [github.com/new](https://github.com/new)
   - Name it (e.g., `pdf-qa-bot`)
   - Choose public or private
   - Click "Create repository"

2. **Push your code to GitHub**

```bash
cd /path/to/pdfq&a

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: PDF Q&A Bot with Gemini AI"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

3. **Verify files are uploaded**
   - Check that `app.py`, `requirements.txt`, and `utils/` folder are present
   - Ensure `.env` is NOT uploaded (it should be in `.gitignore`)

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Navigate to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your GitHub repository
   - Choose the branch (usually `main`)
   - Set main file path: `app.py`

3. **Configure Advanced Settings** (Click "Advanced settings")
   - Python version: `3.10` or higher
   - Leave other settings as default

4. **Add Secrets** (IMPORTANT!)
   - In the "Secrets" section, add:
   ```toml
   GOOGLE_API_KEY = "your_actual_gemini_api_key_here"
   ```
   - Replace with your actual API key
   - Click outside the text box to save

5. **Deploy**
   - Click "Deploy" button
   - Wait for deployment (usually 2-5 minutes)

### Step 3: Verify Deployment

1. **Check build logs**
   - Monitor the deployment logs for any errors
   - Common issues: missing dependencies, syntax errors

2. **Test the application**
   - Once deployed, test by:
     - Uploading a sample PDF
     - Processing it
     - Asking a test question

3. **Access your app**
   - Your app URL: `https://YOUR_APP_NAME.streamlit.app`
   - Share this URL with others!

## ⚙️ Managing Your Deployed App

### Update Secrets

1. Go to your app on Streamlit Cloud
2. Click on the menu (⋮) → "Settings"
3. Go to "Secrets" section
4. Update your `GOOGLE_API_KEY` if needed
5. Click "Save"

### Update Code

1. **Make changes locally**
   ```bash
   # Edit your files
   git add .
   git commit -m "Description of changes"
   git push
   ```

2. **Automatic redeployment**
   - Streamlit Cloud automatically redeploys when you push to GitHub
   - Watch the build logs in your app dashboard

### View Logs

1. Go to your app dashboard
2. Click "Manage app" → "Logs"
3. View real-time logs for debugging

### Restart App

If your app becomes unresponsive:
1. Go to app dashboard
2. Click menu (⋮) → "Reboot"

## 🔒 Security Best Practices

### Protecting Your API Key

1. **Never commit secrets to Git**
   - Always use Streamlit Cloud secrets
   - Verify `.env` is in `.gitignore`

2. **Use environment variables**
   - In Streamlit Cloud: Use the Secrets management
   - Locally: Use `.env` file (not committed)

3. **Rotate keys regularly**
   - Generate new API keys periodically
   - Update in Streamlit Cloud secrets

### Repository Settings

1. **Private vs Public**
   - If your repo is public, NEVER include API keys in code
   - Consider making repo private if dealing with sensitive data

2. **Branch Protection**
   - Enable branch protection on `main`
   - Require pull request reviews

## 🐛 Troubleshooting Deployment

### Issue: "ModuleNotFoundError"

**Cause**: Missing dependency in `requirements.txt`

**Solution**:
```bash
# Add missing package to requirements.txt
pip freeze | grep package_name >> requirements.txt
git commit -am "Add missing dependency"
git push
```

### Issue: "API Key Error"

**Cause**: Secret not configured correctly

**Solution**:
1. Go to Streamlit Cloud → Your App → Settings → Secrets
2. Ensure format is:
   ```toml
   GOOGLE_API_KEY = "your_key_here"
   ```
3. No extra quotes or spaces
4. Click "Save" and reboot app

### Issue: "Build Failed"

**Cause**: Syntax error or incompatible dependencies

**Solution**:
1. Check build logs for specific error
2. Test locally first: `streamlit run app.py`
3. Ensure Python version compatibility
4. Check `requirements.txt` for version conflicts

### Issue: "App Crashes on PDF Upload"

**Cause**: Memory limit or large file

**Solution**:
1. Streamlit Cloud free tier has memory limits
2. Test with smaller PDFs first
3. Consider upgrading to paid tier for larger files
4. Optimize chunk sizes in code

### Issue: "Slow Response Times"

**Cause**: Cold start or API rate limits

**Solution**:
1. First request after inactivity is slower (cold start)
2. Check Gemini API rate limits
3. Optimize number of chunks retrieved (`top_k`)
4. Consider caching strategies

## 📊 Monitoring

### Usage Statistics

- Streamlit Cloud provides basic analytics
- View in app dashboard → Analytics

### API Usage

- Monitor Gemini API usage: [Google Cloud Console](https://console.cloud.google.com)
- Set up billing alerts
- Track quota limits

## 💰 Cost Considerations

### Streamlit Cloud

- **Free Tier**: Limited resources, public apps
- **Paid Tier**: More resources, private apps, custom domains

### Google Gemini API

- **Free Tier**: Generous limits for testing
- **Paid Tier**: Pay-per-use for production
- Check current pricing: [Google AI Pricing](https://ai.google.dev/pricing)

## 🔄 Continuous Integration (Optional)

### GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 🌟 Production Tips

1. **Test Thoroughly Locally** before deploying
2. **Use Version Pinning** in `requirements.txt`
3. **Monitor Errors** regularly in logs
4. **Set Up Alerts** for app downtime
5. **Document Changes** in commit messages
6. **Keep Dependencies Updated** for security
7. **Backup Your Data** if storing user information
8. **Plan for Scale** if expecting high traffic

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [FAISS Documentation](https://faiss.ai/)
- [Streamlit Forums](https://discuss.streamlit.io/)

## 🆘 Getting Help

If you encounter issues:

1. Check build logs in Streamlit Cloud
2. Review error messages carefully
3. Search Streamlit Community forums
4. Check GitHub Issues
5. Review this troubleshooting guide

---

**Happy Deploying! 🚀**

