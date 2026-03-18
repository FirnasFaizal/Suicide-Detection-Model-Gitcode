# MindSafe - Suicide Detection with Empathetic AI Response

A production-ready web application that uses a pretrained DistilBERT model to detect suicidal thoughts in text and generates empathetic responses using Google's Gemini API.

## 🏗️ Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── gemini_service.py      # Gemini AI integration
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/                  # React + Vite + TypeScript frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── contexts/         # Theme context
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   ├── public/              # Static assets
│   └── package.json         # Node dependencies
├── model/                    # Pretrained model files
│   ├── tf_model.h5
│   ├── config.json
│   └── tokenizer files
└── MODEL_NOTES.md           # Model documentation
```

## ✨ Features

- **Suicide Detection**: Uses pretrained DistilBERT model (90.94% accuracy)
- **Empathetic AI Responses**: Context-aware responses via Gemini API
- **Modern UI**: Clean, minimal design with light/dark theme
- **Responsive**: Mobile-friendly interface
- **Real-time Analysis**: Instant text analysis with confidence scores
- **Crisis Resources**: Automatic helpline information for at-risk users
- **Typewriter Effect**: Smooth text animation for AI responses
- **Error Handling**: Graceful error boundaries and user-friendly messages

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Google Gemini API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

6. Run the server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Start development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to `backend/.env`

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns server status and model loading state.

### Predict
```
POST /predict
Body: { "text": "your text here" }
Response: { "label": "suicide" | "non-suicide", "confidence": 0.95 }
```

### Analyze (with AI Response)
```
POST /analyze
Body: { "text": "your text here" }
Response: {
  "label": "suicide" | "non-suicide",
  "confidence": 0.95,
  "response": "empathetic AI response"
}
```

## 🎨 Design Specifications

### Color Palette

**Light Mode:**
- Background: `#fafafa`
- Card: `#ffffff`
- Primary: `#6366f1` (Indigo)
- Text: `#1e293b`

**Dark Mode:**
- Background: `#0a0a0a`
- Card: `#141414`
- Primary: `#818cf8` (Light Indigo)
- Text: `#f1f5f9`

### Typography
- Font: Inter (Google Fonts)
- Headings: 600-700 weight
- Body: 400-500 weight

### Components

1. **Header**: App title and tagline
2. **ThemeToggle**: Sun/moon icon, top-right position
3. **TextInputPanel**: Large textarea with character counter
4. **LoadingState**: Animated spinner with pulsing text
5. **ResultCard**: Confidence meter with color coding
6. **ResponsePanel**: Typewriter animation with crisis resources
7. **ErrorBoundary**: Graceful error handling

## 🧪 Testing

### Backend
```bash
cd backend
# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling great today!"}'
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

## 📦 Production Build

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
npm run preview
```

## 🔒 Security Considerations

- API keys stored in environment variables (never committed)
- Input validation and sanitization
- CORS configured for specific origins
- Error messages don't expose sensitive information
- Rate limiting recommended for production

## 🎯 Model Performance

- **Accuracy**: 90.94%
- **Precision**: 86.75%
- **Recall**: 96.93%
- **F1 Score**: 91.56%

Note: Higher false positive rate is intentional for safety.

## 📱 Crisis Resources

**India:**
- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345

## 🤝 Contributing

This is a production-ready application. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Important Notes

- This tool is NOT a replacement for professional mental health care
- Always encourage users to seek professional help
- Model predictions should be used as supportive information only
- Ensure compliance with local healthcare regulations

## 📄 License

See original repository for license information.

## 👥 Original Model Authors

- Muhammed Firnas Faizal
- Ansh Mohan Srivastava

## 🙏 Acknowledgments

- Dataset: [Suicide and Depression Detection](https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch)
- Model: DistilBERT (HuggingFace)
- AI: Google Gemini API
