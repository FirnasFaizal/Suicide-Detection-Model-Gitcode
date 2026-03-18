from __future__ import annotations

from dataclasses import dataclass


GENERAL_DISCLAIMER = (
    "MindSafe offers supportive conversation and automated screening when the pretrained classifier is "
    "available. It is not a substitute for professional mental health care, diagnosis, or emergency support."
)


@dataclass(frozen=True)
class SupportResource:
    title: str
    contact: str
    description: str


SUPPORT_RESOURCES = [
    SupportResource(
        title="Emergency services",
        contact="Call your local emergency number",
        description="Use this right away if there is immediate danger, you may act on self-harm thoughts, or someone cannot stay safe.",
    ),
    SupportResource(
        title="988 Suicide & Crisis Lifeline",
        contact="Call or text 988 (US and Canada)",
        description="24/7 crisis support for suicidal thoughts, emotional distress, or concern for someone else.",
    ),
    SupportResource(
        title="Samaritans",
        contact="Call 116 123 (UK and ROI)",
        description="Free listening support any time, day or night.",
    ),
    SupportResource(
        title="iCall",
        contact="Call 9152987821 (India)",
        description="Mental health counseling and emotional support line.",
    ),
    SupportResource(
        title="Trusted person",
        contact="Reach out to someone who can stay with you",
        description="If you feel at risk, contact a friend, family member, roommate, neighbor, or another trusted person who can help you get immediate support.",
    ),
]


def status_headline(model_available: bool) -> str:
    if model_available:
        return "Screening and supportive response are available"
    return "Supportive response is available while screening is offline"


def guidance_title(label: str | None) -> str:
    if label == "suicide":
        return "Please focus on immediate human support right now"
    if label == "non-suicide":
        return "Supportive guidance"
    return "Supportive conversation only"


def care_recommendation(label: str | None, model_available: bool) -> str:
    if not model_available:
        return (
            "The screening model is temporarily unavailable, so this reply is supportive conversation only. "
            "If you feel unsafe or at risk of harming yourself, contact emergency services or a crisis line now."
        )

    if label == "suicide":
        return (
            "The classifier detected language that may indicate elevated suicide risk. Prioritize immediate human help, "
            "including a crisis line, emergency services, or a trusted person who can stay with you."
        )

    return (
        "No high-risk suicide language was detected in this message, but that is not a diagnosis or a guarantee of safety. "
        "Professional support can still be helpful if things feel overwhelming."
    )


def model_unavailable_message() -> str:
    return (
        "Automated screening is temporarily unavailable because the pretrained detection model is not loaded. "
        "You can still use MindSafe for supportive conversation, but no risk assessment has been performed."
    )
