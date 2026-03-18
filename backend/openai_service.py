from __future__ import annotations

import logging
from typing import Optional

from config import settings
from fallback_responses import get_fallback_response
from model_service import DetectionResult

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - depends on local environment
    OpenAI = None


logger = logging.getLogger(__name__)


def _clean_message(value: str, limit: int = 900) -> str:
    normalized = " ".join(value.split())
    return normalized[:limit].strip()


class OpenAIService:
    def __init__(self) -> None:
        self.client = None
        self.available = False
        self.status_message = "LLM support not initialized."

        if not settings.llm_api_key:
            self.status_message = "LLM API key not configured. Using predefined empathetic fallback responses."
            return

        if OpenAI is None:
            self.status_message = "openai package not installed. Using predefined empathetic fallback responses."
            return

        try:
            self.client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
            self.available = True
            self.status_message = f"{settings.llm_provider} ready with model {settings.llm_model}."
        except Exception as exc:  # pragma: no cover - runtime only
            self.status_message = f"{settings.llm_provider} unavailable: {exc}"
            logger.exception("Failed to initialize LLM client")

    def generate_supportive_response(
        self,
        *,
        text: str,
        detection: Optional[DetectionResult],
        model_available: bool,
        conversation: list[dict[str, str]] | None = None,
    ) -> str:
        if not self.available or self.client is None:
            return get_fallback_response(detection.label if detection else None, model_available)

        system_prompt, user_prompt = self._build_prompt(
            text=text,
            detection=detection,
            model_available=model_available,
            conversation=conversation or [],
        )

        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                temperature=0.5,
                max_tokens=220,
                timeout=20,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            message = response.choices[0].message.content if response.choices else ""
            cleaned = (message or "").strip()
            if cleaned:
                return cleaned
            logger.warning("LLM returned an empty response. Using predefined fallback response.")
        except Exception as exc:  # pragma: no cover - runtime only
            error_message = str(exc)
            if "invalid_api_key" in error_message or "Incorrect API key provided" in error_message:
                self.available = False
                self.status_message = f"{settings.llm_provider} API key was rejected. Using predefined empathetic fallback responses."
            elif "insufficient_quota" in error_message or "exceeded your current quota" in error_message:
                self.available = False
                self.status_message = f"{settings.llm_provider} quota is unavailable. Using predefined empathetic fallback responses."
            elif "timeout" in error_message.lower():
                self.status_message = f"{settings.llm_provider} timed out. Using predefined empathetic fallback responses."
            logger.exception("LLM response generation failed: %s", exc)

        return get_fallback_response(detection.label if detection else None, model_available)

    def _build_prompt(
        self,
        *,
        text: str,
        detection: Optional[DetectionResult],
        model_available: bool,
        conversation: list[dict[str, str]],
    ) -> tuple[str, str]:
        transcript = self._format_conversation(conversation)
        system_prompt = (
            "You write calm, professional, empathetic responses for a mental health support application. "
            "You are not a therapist, clinician, or emergency service. Keep replies to at most two short paragraphs. "
            "Avoid diagnosis, guarantees, manipulative wording, cheerleading, or playful language."
        )

        if not model_available:
            return (
                system_prompt,
                f"""
The automated suicide-risk screening classifier is unavailable.

Rules:
- Do not claim the message was screened, analyzed, assessed, or classified.
- Do not mention confidence, labels, or verdicts.
- Offer supportive, non-diagnostic conversation only.
- Encourage immediate human help if the person feels unsafe or may harm themselves.

Recent conversation:
{transcript}

User message:
"{_clean_message(text)}"
""".strip(),
            )

        if detection and detection.label == "suicide":
            return (
                system_prompt,
                f"""
A separate pretrained classifier flagged elevated suicide risk in the user's latest message.

Rules:
- Do not offer diagnosis or certainty.
- Acknowledge pain directly and compassionately.
- Encourage immediate contact with crisis support, a trusted person, or emergency services if there is imminent danger.
- State that the person does not have to handle this alone.

Recent conversation:
{transcript}

User message:
"{_clean_message(text)}"
""".strip(),
            )

        return (
            system_prompt,
            f"""
A separate pretrained classifier did not detect high-risk suicide language in the latest message.

Rules:
- Do not present this as a diagnosis or guarantee of safety.
- Acknowledge the user's feelings and offer grounded encouragement.
- Suggest reaching out for professional support if things feel hard or overwhelming.

Recent conversation:
{transcript}

User message:
"{_clean_message(text)}"
""".strip(),
        )

    def _format_conversation(self, conversation: list[dict[str, str]]) -> str:
        if not conversation:
            return "No prior conversation available."

        formatted: list[str] = []
        for message in conversation[-6:]:
            role = message.get("role", "user").strip().lower()
            speaker = "User" if role == "user" else "Assistant"
            content = _clean_message(message.get("content", ""), limit=280)
            if content:
                formatted.append(f"- {speaker}: {content}")

        return "\n".join(formatted) if formatted else "No prior conversation available."
