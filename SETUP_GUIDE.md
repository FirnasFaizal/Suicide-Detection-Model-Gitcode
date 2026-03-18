# Quick Setup Guide

## 🎯 Quick Start (Recommended)

### Option 1: Automated Setup (macOS/Linux)

```bash
# Make the start script executable
chmod +x start.sh

# Run the setup and start script
./start.sh
```

The script will:
- Create environment files if missing
- Set up Python virtual environment
- Install all dependencies
- Start both backend and frontend servers

### Option 2: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Add your Gemini API key to .env
# Edit .env and add: GEMINI_API_KEY=your_key_here

# 6. Start server
python main.py
```

Backend runs on: http://localhost:8000

#### Frontend Setup

```bash
# 1. Open new terminal and navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
cp .env.example .env

# 4. Start development server
npm run dev
```

Frontend runs on: http://localhost:5173

## 🔑 Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Paste into `backend/.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

## ✅ Verify Installation

### Test Backend
```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy","model_loaded":true}
```

### Test Frontend
Open browser to http://localhost:5173

## 🐛 Troubleshooting

### Backend Issues

**Model not loading:**
```bash
# Ensure model files exist
ls -la model/

# Should see: tf_model.h5, config.json, tokenizer files
```

**Port 8000 already in use:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Missing dependencies:**
```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Kill process
lsof -ti:5173 | xargs kill -9
```

**Module not found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear cache and rebuild
npm run build -- --force
```

### Common Issues

**CORS errors:**
- Ensure backend is running on port 8000
- Check `VITE_API_BASE_URL` in `frontend/.env`

**Gemini API errors:**
- Verify API key is correct in `backend/.env`
- Check API quota at Google AI Studio
- Ensure no extra spaces in .env file

**Model loading slow:**
- First load takes 30-60 seconds (normal)
- Model is cached after first load

## 📦 Production Deployment

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
# Serve the dist/ folder with your preferred static server
```

## 🔒 Security Checklist

- [ ] Never commit .env files
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS in production
- [ ] Configure CORS for production domains
- [ ] Add rate limiting
- [ ] Set up monitoring and logging

## 📚 Next Steps

1. Test the application with sample inputs
2. Customize the UI colors/theme
3. Add additional crisis resources for your region
4. Set up error monitoring (Sentry, etc.)
5. Configure production deployment

## 💡 Tips

- Use incognito mode to test without cached data
- Check browser console for frontend errors
- Check terminal for backend errors
- Model predictions take 1-3 seconds
- Gemini responses take 2-5 seconds

## 🆘 Need Help?

- Check MODEL_NOTES.md for model details
- Review PROJECT_README.md for full documentation
- Ensure all dependencies are installed
- Verify Python 3.8+ and Node 18+ are installed
