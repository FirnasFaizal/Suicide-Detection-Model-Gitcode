# MindSafe

MindSafe is a suicide-risk support application with a split FastAPI + React architecture.

- The pretrained ML model is the only authority for automated suicide-risk detection.
- An external LLM provider is used only for empathetic conversational responses.
- If the pretrained model is unavailable, the app switches to a transparent support-only mode and does not produce a suicide-risk verdict.
- MindSafe is not a substitute for professional mental health care, diagnosis, or emergency services.

## Architecture

- `backend/` - FastAPI API, model loading, LLM integration, safety response shaping
- `frontend/` - React + Vite client with chat UI, screening state, and crisis resources
- `model/` - pretrained classifier assets loaded by the backend

Legacy files such as `app.py` and `simple_app.py` are not the primary application path.

## Setup

### 1. Install dependencies

```bash
./install.sh
```

### 2. Configure environment variables

Backend example in `backend/.env.example`:

```bash
LLM_API_KEY=your_key_here
LLM_MODEL=speakleash/bielik-11b-v2.6-instruct
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_PROVIDER=nvidia-integrate
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
MODEL_DIR=../model
PORT=8000
```

Frontend example in `frontend/.env.example`:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Create local files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Never commit real API keys.

The classifier artifacts in `model/` were exported from a TensorFlow/Hugging Face setup that matches `transformers==4.28.0` and TensorFlow/Keras 2.x, which are pinned in the backend requirements.

### 3. Run locally

```bash
./start.sh
```

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/health`

## Full detection vs degraded mode

### Full detection mode

The backend will perform real ML screening only when the actual model weights are present in `model/`.

This repo tracks the model through Git LFS. If you only have pointer files, run:

```bash
git lfs install
git lfs pull
```

### Support-only degraded mode

If the model is missing or fails to load:

- the backend still starts
- `/health` reports `model_available: false`
- `/analyze` returns `status: "model_unavailable"`
- no label, confidence, or suicide-risk verdict is returned
- The configured LLM may still provide empathetic conversation, or the backend uses built-in supportive fallback text
- crisis and support resources remain visible in the UI

## API summary

- `GET /health` - service readiness, including `model_available`
- `POST /predict` - ML detection only when the classifier is available
- `POST /analyze` - screening + supportive response, or support-only mode when screening is unavailable

### `POST /analyze` request shape

```json
{
  "text": "I feel overwhelmed and do not know what to do.",
  "conversation": [
    { "role": "user", "content": "I have had a very hard week." },
    { "role": "assistant", "content": "I am here with you. What feels hardest today?" }
  ]
}
```

- `text` is the latest user message and remains the only message screened by the pretrained classifier.
- `conversation` is optional recent chat context used only to help the configured LLM write a more coherent empathetic reply.
- The configured LLM still does not decide the risk classification.

## Safety notes

- High-risk detections trigger urgent, supportive guidance and crisis-support information
- When the classifier is unavailable, the app explicitly says no automated screening took place
- The configured LLM never replaces the classifier and never receives authority to make a risk verdict
- The UI avoids presenting the system as a substitute for licensed care or emergency help
- Recent conversation context is used only for empathy and continuity, not for classifier authority
