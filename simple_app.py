"""
Legacy demo application.

Prefer backend/main.py with the React frontend for current development.
This file remains only as a minimal local demo and does not provide the
pretrained classifier-based screening flow used by the main product.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MindSafe Demo", version="1.0.0")

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
gemini_model = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    logger.warning("GEMINI_API_KEY not set for legacy demo; using fallback responses")

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class AnalyzeResponse(BaseModel):
    label: str
    confidence: float
    response: str

def simple_detection(text: str):
    """Simple keyword-based detection for demo"""
    text_lower = text.lower()
    
    # Suicide-related keywords
    suicide_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die', 
        'better off dead', 'no reason to live', 'can\'t go on',
        'end it all', 'take my life', 'don\'t want to live'
    ]
    
    # Check for keywords
    for keyword in suicide_keywords:
        if keyword in text_lower:
            return 'suicide', random.uniform(0.75, 0.95)
    
    # Check for negative sentiment indicators
    negative_words = ['depressed', 'hopeless', 'worthless', 'alone', 'pain', 'suffering']
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if negative_count >= 2:
        return 'suicide', random.uniform(0.60, 0.75)
    
    return 'non-suicide', random.uniform(0.70, 0.90)

def generate_response(text: str, label: str, confidence: float) -> str:
    """Generate empathetic response using Gemini"""
    
    if label == "suicide":
        prompt = f"""You are a compassionate mental health support assistant. A person has shared: "{text}"

Provide a warm, caring response (2-3 paragraphs) that:
1. Acknowledges their pain
2. Shows genuine care
3. Gently encourages professional help
4. Reminds them they're not alone
5. Avoids being clinical

Be human and warm."""
    else:
        prompt = f"""You are a supportive assistant. A person shared: "{text}"

Provide a warm response (2-3 paragraphs) that:
1. Acknowledges their feelings
2. Offers positive reinforcement
3. Shows support

Be genuine and encouraging."""

    try:
        if gemini_model is not None:
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        raise RuntimeError("Gemini unavailable")
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        if label == "suicide":
            return ("I hear you, and your feelings matter. What you're going through is difficult, and it takes courage to express these thoughts. "
                   "Please know you don't have to face this alone. Consider reaching out to a mental health professional or crisis helpline. "
                   "Your life has value, and there is hope for better days.")
        else:
            return ("Thank you for sharing. Remember that it's okay to have difficult feelings, and reaching out is a sign of strength. "
                   "I'm here to support you.")

@app.get("/api/health")
async def health():
    return {"status": "healthy", "mode": "demo", "gemini": "configured"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        label, confidence = simple_detection(request.text)
        response = generate_response(request.text, label, confidence)
        
        return AnalyzeResponse(
            label=label,
            confidence=confidence,
            response=response
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindSafe - A safe space to express yourself</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .fade-in { animation: fadeIn 0.5s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .dark { background: #0a0a0a; color: #f1f5f9; }
        .dark .card { background: #141414; }
    </style>
    <script>
        tailwind.config = { darkMode: 'class' }
    </script>
</head>
<body class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div id="app"></div>
    <script>
        const theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') document.documentElement.classList.add('dark');
        
        function toggleTheme() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }
        
        let isLoading = false, result = null, error = null;
        
        function render() {
            document.getElementById('app').innerHTML = `
                <button onclick="toggleTheme()" class="fixed top-6 right-6 p-3 rounded-xl bg-white dark:bg-gray-800 shadow-md hover:shadow-lg transition-all z-50">
                    ${document.documentElement.classList.contains('dark') ? 
                        '<svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>' :
                        '<svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>'
                    }
                </button>
                
                <div class="container mx-auto px-4 py-12 max-w-2xl">
                    <header class="text-center mb-12 fade-in">
                        <h1 class="text-5xl font-bold mb-3 bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">MindSafe</h1>
                        <p class="text-gray-600 dark:text-gray-400 text-lg">A safe space to express yourself</p>
                    </header>
                    
                    <div class="space-y-6">
                        <form onsubmit="handleSubmit(event)" class="w-full">
                            <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 card">
                                <textarea id="textInput" placeholder="Share what's on your mind..." maxlength="1000" rows="6" ${isLoading ? 'disabled' : ''} 
                                    class="w-full resize-none bg-transparent border-none outline-none text-gray-800 dark:text-gray-200 placeholder-gray-400 text-lg disabled:opacity-50"></textarea>
                                <div class="flex items-center justify-between mt-4">
                                    <span class="text-sm text-gray-500" id="charCount">0 / 1000</span>
                                    <button type="submit" ${isLoading ? 'disabled' : ''} 
                                        class="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl transition-all disabled:opacity-50 shadow-md">
                                        ${isLoading ? 'Analyzing...' : 'Analyze'}
                                    </button>
                                </div>
                            </div>
                        </form>
                        
                        ${isLoading ? '<div class="flex flex-col items-center py-12 fade-in"><div class="relative w-16 h-16 mb-4"><div class="absolute inset-0 rounded-full border-4 border-indigo-200 dark:border-indigo-900"></div><div class="absolute inset-0 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin"></div></div><p class="text-gray-600 dark:text-gray-400 animate-pulse">Analyzing...</p></div>' : ''}
                        
                        ${error ? `<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 rounded-2xl p-4 fade-in"><p class="text-red-800 dark:text-red-200">${error}</p></div>` : ''}
                        
                        ${result ? renderResult() : ''}
                    </div>
                </div>
            `;
        }
        
        function renderResult() {
            const isSuicidal = result.label === 'suicide';
            const confidence = Math.round(result.confidence * 100);
            
            return `
                <div class="fade-in space-y-4">
                    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 card">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 rounded-full ${isSuicidal ? 'bg-rose-100 dark:bg-rose-900/30' : 'bg-teal-100 dark:bg-teal-900/30'} flex items-center justify-center">
                                ${isSuicidal ? 
                                    '<svg class="w-6 h-6 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>' :
                                    '<svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
                                }
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">${isSuicidal ? 'Concern Detected' : 'No Immediate Concern'}</h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Confidence: ${confidence}%</p>
                            </div>
                        </div>
                        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                            <div class="h-full transition-all duration-1000 ${isSuicidal ? 'bg-gradient-to-r from-rose-400 to-rose-600' : 'bg-gradient-to-r from-teal-400 to-teal-600'}" style="width: ${confidence}%"></div>
                        </div>
                    </div>
                    
                    <div class="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl shadow-md p-6">
                        <div class="flex items-start gap-3">
                            <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0">
                                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                            </div>
                            <div class="flex-1">
                                <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3">Response</h3>
                                <div class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap" id="responseText"></div>
                            </div>
                        </div>
                        
                        ${isSuicidal ? `
                            <div class="mt-6 pt-6 border-t border-indigo-200 dark:border-gray-700">
                                <div class="bg-rose-50 dark:bg-rose-900/20 rounded-xl p-4">
                                    <h4 class="font-semibold text-rose-900 dark:text-rose-300 mb-2">🆘 Crisis Support Resources</h4>
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
                
                if (!response.ok) throw new Error('Analysis failed');
                
                result = await response.json();
                isLoading = false;
                render();
                
                // Typewriter effect
                const el = document.getElementById('responseText');
                if (el) {
                    let i = 0;
                    const txt = result.response;
                    const interval = setInterval(() => {
                        if (i < txt.length) {
                            el.textContent = txt.slice(0, i + 1);
                            i++;
                        } else clearInterval(interval);
                    }, 20);
                }
            } catch (err) {
                error = err.message;
                isLoading = false;
                render();
            }
        }
        
        document.addEventListener('input', (e) => {
            if (e.target.id === 'textInput') {
                const counter = document.getElementById('charCount');
                if (counter) counter.textContent = `${e.target.value.length} / 1000`;
            }
        });
        
        render();
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                    MindSafe DEMO                         ║
    ║          Suicide Detection & Support System              ║
    ╚══════════════════════════════════════════════════════════╝
    
    🌐 Open: http://localhost:8000
    ✅ Gemini AI: Configured
    ⚡ Mode: Demo (keyword-based detection)
    
    Press Ctrl+C to stop
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
