# Start Here

Use the split application in `backend/` + `frontend/`.

## Quick start

```bash
./install.sh
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
./start.sh
```

## Gemini setup

Add your key to `backend/.env`:

```bash
GEMINI_API_KEY=your_key_here
```

Never hardcode or commit the key.

## Important: model files

Full suicide-risk screening requires the actual pretrained model weights from Git LFS.

If you see that `model/tf_model.h5` is only a tiny pointer file, run:

```bash
git lfs install
git lfs pull
```

## What happens if the model is missing?

MindSafe still starts safely in support-only mode:

- the frontend remains usable
- supportive conversation still works
- general crisis/support resources are shown
- no suicide-risk label or confidence score is returned
- the UI clearly says screening is temporarily unavailable
