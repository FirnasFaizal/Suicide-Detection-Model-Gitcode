from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent

load_dotenv(BASE_DIR / ".env")
load_dotenv(REPO_ROOT / ".env")


def _split_csv(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    port: int
    allowed_origins: list[str]
    llm_api_key: str
    llm_model: str
    llm_base_url: str
    llm_provider: str
    model_dir: Path


settings = Settings(
    app_name="MindSafe API",
    app_version="2.0.0",
    port=int(os.getenv("PORT", "8000")),
    allowed_origins=_split_csv(
        os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
        )
    ),
    llm_api_key=os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip(),
    llm_model=os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", "speakleash/bielik-11b-v2.6-instruct")),
    llm_base_url=os.getenv("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1").strip(),
    llm_provider=os.getenv("LLM_PROVIDER", "nvidia-integrate").strip(),
    model_dir=Path(os.getenv("MODEL_DIR", str(REPO_ROOT / "model"))).resolve(),
)
