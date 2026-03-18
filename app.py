"""
MindSafe - Integrated Suicide Detection Application
Combines model inference, Gemini AI, and web interface in one file
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import pipeline
import google.generativeai as genai
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="MindSafe", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    logger.warning("GEMINI_API_KEY not set - AI responses will use fallback")
    gemini_model = None

# Load model at startup
model_pipeline = None

@app.on_event("startup")
async def load_model():
    """Load the pretrained model once at startup"""
    global model_pipeline
    try:
        logger.info("Loading suicide detection model...")
        model_pipeline = pipeline(
            'sentiment-analysis',
            model='./model',
            tokenizer='./model'
        )
        logger.info("✓ Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.info("Model will need to be loaded manually")

# Request/Response models
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class AnalyzeResponse(BaseModel):
    label: str
    confidence: float
    response: str

def generate_empathetic_response(text: str, label: str, confidence: float) -> str:
    """Generate empathetic response using Gemini or fallback"""
    
    if label == "suicide":
        prompt = f"""You are a compassionate mental health support assistant. A person has shared the following message that indicates they may be experiencing suicidal thoughts:

"{text}"

Please provide a warm, caring, and non-judgmental response that:
1. Acknowledges their pain and validates their feelings
2. Expresses genuine care and concern
3. Gently encourages them to reach out for professional help
4. Reminds them they are not alone
5. Avoids being clinical, cold, or dismissive
6. Keeps the response concise (2-3 paragraphs maximum)

Remember: Be human, be warm, and show that you care."""
    else:
        prompt = f"""You are a supportive mental health assistant. A person has shared the following message:

"{text}"

Please provide a warm and positive response that:
1. Acknowledges their feelings with empathy
2. Offers positive reinforcement
3. Shows understanding and support
4. Keeps the tone warm but not overdone
5. Keeps the response concise (2-3 paragraphs maximum)

Remember: Be genuine, supportive, and encouraging."""

    # Try Gemini API
    if gemini_model:
        try:
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
    
    # Fallback responses
    if label == "suicide":
        return ("I hear you, and I want you to know that your feelings matter. What you're going through is incredibly difficult, "
               "and it takes courage to express these thoughts. Please know that you don't have to face this alone. "
               "There are people who care and want to help. Consider reaching out to a mental health professional or a crisis helpline. "
               "Your life has value, and there is hope for better days ahead.")
    else:
        return ("Thank you for sharing your thoughts with me. I appreciate your openness. "
               "Remember that it's okay to have difficult feelings, and reaching out is a sign of strength. "
               "I'm here to support you, and I hope you continue to take care of yourself.")

# API Endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_pipeline is not None,
        "gemini_configured": gemini_model is not None
    }

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyze text and generate empathetic response"""
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check model files in ./model directory")
    
    try:
        # Run prediction
        result = model_pipeline(
            request.text,
            truncation=True,
            max_length=4096
        )[0]
        
        label = result['label']
        confidence = result['score']
        
        # Generate empathetic response
        empathetic_response = generate_empathetic_response(
            text=request.text,
            label=label,
            confidence=confidence
        )
        
        return AnalyzeResponse(
            label=label,
            confidence=confidence,
            response=empathetic_response
        )
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Serve static files and HTML
@app.get("/", response_class=HTMLResponse)
async def serve_app():
    """Serve the main application"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindSafe - A safe space to express yourself</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .fade-in { animation: fadeIn 0.5s ease-in-out; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .dark { background: #0a0a0a; color: #f1f5f9; }
        .dark .card { background: #141414; }
        .typewriter { overflow: hidden; white-space: pre-wrap; }
    </style>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
                }
            }
        }
    </script>
</head>
<body class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    <div id="app"></div>
    
    <script>
        // Theme management
        const theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') document.documentElement.classList.add('dark');
        
        function toggleTheme() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }
        
        // State
        let isLoading = false;
        let result = null;
        let error = null;
        
        // Render functions
        function render() {
            const app = document.getElementById('app');
            app.innerHTML = `
                <button onclick="toggleTheme()" class="fixed top-6 right-6 p-3 rounded-xl bg-white dark:bg-gray-800 shadow-md hover:shadow-lg transition-all duration-300 z-50">
                    ${document.documentElement.classList.contains('dark') ? 
                        '<svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>' :
                        '<svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>'
                    }
                </button>
                
                <div class="container mx-auto px-4 py-12 max-w-2xl">
                    <header class="text-center mb-12 fade-in">
                        <h1 class="text-5xl font-bold mb-3 bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
                            MindSafe
                        </h1>
                        <p class="text-gray-600 dark:text-gray-400 text-lg">A safe space to express yourself</p>
                    </header>
                    
                    <div class="space-y-6">
                        ${renderInput()}
                        ${isLoading ? renderLoading() : ''}
                        ${error ? renderError() : ''}
                        ${result ? renderResult() : ''}
                    </div>
                </div>
            `;
        }
        
        function renderInput() {
            return `
                <form onsubmit="handleSubmit(event)" class="w-full">
                    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 card">
                        <textarea 
                            id="textInput"
                            placeholder="Share what's on your mind..."
                            maxlength="1000"
                            rows="6"
                            ${isLoading ? 'disabled' : ''}
                            class="w-full resize-none bg-transparent border-none outline-none text-gray-800 dark:text-gray-200 placeholder-gray-400 text-lg disabled:opacity-50"
                        ></textarea>
                        <div class="flex items-center justify-between mt-4">
                            <span class="text-sm text-gray-500" id="charCount">0 / 1000</span>
                            <button 
                                type="submit"
                                ${isLoading ? 'disabled' : ''}
                                class="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white font-medium rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
                            >
                                ${isLoading ? 'Analyzing...' : 'Analyze'}
                            </button>
                        </div>
                    </div>
                </form>
            `;
        }
        
        function renderLoading() {
            return `
                <div class="flex flex-col items-center justify-center py-12 fade-in">
                    <div class="relative w-16 h-16 mb-4">
                        <div class="absolute inset-0 rounded-full border-4 border-indigo-200 dark:border-indigo-900"></div>
                        <div class="absolute inset-0 rounded-full border-4 border-indigo-600 dark:border-indigo-400 border-t-transparent animate-spin"></div>
                    </div>
                    <p class="text-gray-600 dark:text-gray-400 animate-pulse">Analyzing your message...</p>
                </div>
            `;
        }
        
        function renderError() {
            return `
                <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl p-4 fade-in">
                    <div class="flex items-start gap-3">
                        <svg class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <div>
                            <h3 class="font-semibold text-red-900 dark:text-red-300 mb-1">Error</h3>
                            <p class="text-sm text-red-800 dark:text-red-200">${error}</p>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function renderResult() {
            const isSuicidal = result.label === 'suicide';
            const confidence = Math.round(result.confidence * 100);
            
            return `
                <div class="w-full fade-in">
                    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 mb-4 card">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-3">
                                <div class="w-12 h-12 rounded-full ${isSuicidal ? 'bg-rose-100 dark:bg-rose-900/30' : 'bg-teal-100 dark:bg-teal-900/30'} flex items-center justify-center">
                                    ${isSuicidal ? 
                                        '<svg class="w-6 h-6 text-rose-600 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>' :
                                        '<svg class="w-6 h-6 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
                                    }
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
                                        ${isSuicidal ? 'Concern Detected' : 'No Immediate Concern'}
                                    </h3>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Confidence: ${confidence}%</p>
                                </div>
                            </div>
                        </div>
                        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                            <div class="h-full transition-all duration-1000 ease-out ${isSuicidal ? 'bg-gradient-to-r from-rose-400 to-rose-600' : 'bg-gradient-to-r from-teal-400 to-teal-600'}" style="width: ${confidence}%"></div>
                        </div>
                    </div>
                    
                    <div class="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl shadow-md p-6 card">
                        <div class="flex items-start gap-3 mb-4">
                            <div class="w-10 h-10 rounded-full bg-indigo-600 dark:bg-indigo-500 flex items-center justify-center flex-shrink-0">
                                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3">Response</h3>
                                <div class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap typewriter" id="responseText"></div>
                            </div>
                        </div>
                        
                        ${isSuicidal ? `
                            <div class="mt-6 pt-6 border-t border-indigo-200 dark:border-gray-700">
                                <div class="bg-rose-50 dark:bg-rose-900/20 rounded-xl p-4">
                                    <h4 class="font-semibold text-rose-900 dark:text-rose-300 mb-2 flex items-center gap-2">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                        </svg>
                                        Crisis Support Resources
                                    </h4>
                                    <div class="text-sm text-rose-800 dark:text-rose-200 space-y-1">
                                        <p><strong>iCall:</strong> 9152987821</p>
                                        <p><strong>Vandrevala Foundation:</strong> 1860-2662-345</p>
                                        <p class="mt-2 text-xs">If you're in crisis, please reach out. Help is available 24/7.</p>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }
        
        // Event handlers
        async function handleSubmit(event) {
            event.preventDefault();
            const text = document.getElementById('textInput').value.trim();
            if (!text || isLoading) return;
            
            isLoading = true;
            error = null;
            result = null;
            render();
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Analysis failed');
                }
                
                result = await response.json();
                isLoading = false;
                render();
                
                // Typewriter effect
                const responseEl = document.getElementById('responseText');
                if (responseEl) {
                    let i = 0;
                    const text = result.response;
                    const interval = setInterval(() => {
                        if (i < text.length) {
                            responseEl.textContent = text.slice(0, i + 1);
                            i++;
                        } else {
                            clearInterval(interval);
                        }
                    }, 20);
                }
            } catch (err) {
                error = err.message;
                isLoading = false;
                render();
            }
        }
        
        // Character counter
        document.addEventListener('input', (e) => {
            if (e.target.id === 'textInput') {
                const count = e.target.value.length;
                const counter = document.getElementById('charCount');
                if (counter) counter.textContent = `${count} / 1000`;
            }
        });
        
        // Initial render
        render();
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                      MindSafe                            ║
    ║          Suicide Detection & Support System              ║
    ╚══════════════════════════════════════════════════════════╝
    
    🌐 Application running at: http://localhost:{port}
    📊 Health check: http://localhost:{port}/api/health
    
    ⚙️  Configuration:
    {'✓' if GEMINI_API_KEY else '✗'} Gemini API Key: {'Configured' if GEMINI_API_KEY else 'Not set (using fallback responses)'}
    
    💡 To set Gemini API key:
       export GEMINI_API_KEY=your_key_here
       
    🔑 Get API key: https://makersuite.google.com/app/apikey
    
    Press Ctrl+C to stop the server
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
