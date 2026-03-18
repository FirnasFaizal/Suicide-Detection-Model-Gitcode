# Quick Start Guide

## 🎯 Three Steps to Run

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Configure (Optional)
```bash
export GEMINI_API_KEY=your_key_here
```
Get key: https://makersuite.google.com/app/apikey

### Step 3: Run
```bash
python app.py
```

Open: http://localhost:8000

## ✅ That's It!

Everything is in one file (`app.py`):
- Backend API
- Model inference
- AI responses
- Web interface

## 🔍 Verify Installation

```bash
# Check health
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","model_loaded":true,"gemini_configured":true}
```

## 💡 Tips

- Works without Gemini API key (uses fallback responses)
- Model loads automatically on startup
- First request may take a few seconds
- Theme persists in browser localStorage

## 🆘 Issues?

**Model not loading:**
- Check `./model/` directory exists
- Verify model files are present

**Port 8000 in use:**
```bash
export PORT=8080
python app.py
```

**Dependencies error:**
```bash
pip install --upgrade -r requirements.txt
```

## 🚀 Next Steps

1. Test with sample inputs
2. Add your Gemini API key for better responses
3. Customize crisis resources for your region
4. Deploy to production (see README.md)
