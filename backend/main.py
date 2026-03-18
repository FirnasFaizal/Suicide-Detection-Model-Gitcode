from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import settings
from model_service import DetectionResult, ModelService
from openai_service import OpenAIService
from safety import (
    GENERAL_DISCLAIMER,
    SUPPORT_RESOURCES,
    care_recommendation,
    guidance_title,
    model_unavailable_message,
    status_headline,
)


model_service = ModelService(settings.model_dir)
llm_service = OpenAIService()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    model_service.load()
    logger.info("Model availability: %s", model_service.model_available)
    logger.info("LLM availability: %s", llm_service.available)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=5000)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Message to analyze or respond to")
    conversation: list[ConversationMessage] = Field(default_factory=list, max_length=12)


class DetectionPayload(BaseModel):
    label: Literal["suicide", "non-suicide"]
    confidence: float
    risk_level: Literal["high", "lower"]
    summary: str
    recommended_action: str


class SupportResourcePayload(BaseModel):
    title: str
    contact: str
    description: str


class AnalyzeResponse(BaseModel):
    status: Literal["screened", "model_unavailable"]
    conversation_mode: Literal["screening", "support_only"]
    model_available: bool
    status_headline: str
    model_status_message: str
    assistant_message: str
    guidance_title: str
    care_recommendation: str
    disclaimer: str
    detection: DetectionPayload | None = None
    support_resources: list[SupportResourcePayload]


class PredictResponse(BaseModel):
    status: Literal["screened", "model_unavailable"]
    model_available: bool
    model_status_message: str
    detection: DetectionPayload | None = None


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    model_available: bool
    status_headline: str
    model_status_message: str
    llm_provider: str
    llm_available: bool
    llm_status_message: str
    conversation_mode: Literal["screening", "support_only"]


def _serialize_detection(detection: DetectionResult) -> DetectionPayload:
    return DetectionPayload(
        label=detection.label,  # type: ignore[arg-type]
        confidence=detection.confidence,
        risk_level=detection.risk_level,  # type: ignore[arg-type]
        summary=detection.summary,
        recommended_action=detection.recommended_action,
    )


def _serialize_resources() -> list[SupportResourcePayload]:
    return [SupportResourcePayload(**resource.__dict__) for resource in SUPPORT_RESOURCES]


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "message": "Use the frontend client for the full experience.",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        model_available=model_service.model_available,
        status_headline=status_headline(model_service.model_available),
        model_status_message=model_service.status_message,
        llm_provider=settings.llm_provider,
        llm_available=llm_service.available,
        llm_status_message=llm_service.status_message,
        conversation_mode="screening" if model_service.model_available else "support_only",
    )


@app.post("/predict", response_model=PredictResponse)
async def predict(request: AnalyzeRequest) -> PredictResponse:
    if not model_service.model_available:
        return PredictResponse(
            status="model_unavailable",
            model_available=False,
            model_status_message=model_service.status_message,
            detection=None,
        )

    detection = model_service.analyze(request.text)
    return PredictResponse(
        status="screened",
        model_available=True,
        model_status_message=model_service.status_message,
        detection=_serialize_detection(detection),
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    detection = model_service.analyze(request.text) if model_service.model_available else None
    assistant_message = llm_service.generate_supportive_response(
        text=request.text,
        detection=detection,
        model_available=model_service.model_available,
        conversation=[message.model_dump() for message in request.conversation],
    )

    status: Literal["screened", "model_unavailable"] = (
        "screened" if model_service.model_available else "model_unavailable"
    )

    return AnalyzeResponse(
        status=status,
        conversation_mode="screening" if model_service.model_available else "support_only",
        model_available=model_service.model_available,
        status_headline=status_headline(model_service.model_available),
        model_status_message=(
            model_service.status_message
            if model_service.model_available
            else f"{model_unavailable_message()} {model_service.status_message}"
        ),
        assistant_message=assistant_message,
        guidance_title=guidance_title(detection.label if detection else None),
        care_recommendation=care_recommendation(detection.label if detection else None, model_service.model_available),
        disclaimer=GENERAL_DISCLAIMER,
        detection=_serialize_detection(detection) if detection else None,
        support_resources=_serialize_resources(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)
