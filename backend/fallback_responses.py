from __future__ import annotations

import random


HIGH_RISK_RESPONSES = [
    "Hey... I'm really sorry you're feeling like this. I can't fully know what it's like for you, but I can hear how heavy it feels. You don't have to carry all of this by yourself right now--I'm here with you.",
    "That sounds really overwhelming. Like things have just been piling up and you haven't had space to breathe. I'm really glad you said something instead of keeping it all inside.",
    "I'm really sorry you're going through this. It makes sense that you'd feel exhausted if you've been dealing with so much. You don't have to figure everything out tonight--just being here and talking is enough.",
    "Hey, I'm here. You don't have to explain everything perfectly or have the right words. Just tell me what it feels like--I'm listening.",
    "That sounds really painful. And honestly, it's okay that it hurts this much--what you're going through isn't small. You're allowed to feel this.",
    "I can hear how tired you are... not just physically, but emotionally. Like everything is just weighing on you. I'm really glad you reached out instead of staying alone with it.",
    "I'm really glad you told me. Seriously. Even if it feels messy or confusing, it matters. You matter.",
    "I wish I could take some of this weight off you. Since I can't, I'll stay here with you while you talk through it. You don't have to go through this moment alone.",
    "Hey... slow down for a second. You're allowed to pause. You don't have to solve everything right now. Let's just take this one moment at a time.",
    "If it feels even a little possible, maybe think about someone you trust who could sit with you through this too. You deserve more than just carrying this alone.",
    "I care about what you're going through. You're not just another conversation--you're someone who deserves support, understanding, and patience.",
    "If things ever start to feel like too much to handle on your own, it's really important to reach out to someone nearby or a helpline. You deserve real support in those moments.",
]

LOWER_RISK_RESPONSES = [
    "That sounds really overwhelming. Like things have just been piling up and you haven't had space to breathe. I'm really glad you said something instead of keeping it all inside.",
    "I'm really sorry you're going through this. It makes sense that you'd feel exhausted if you've been dealing with so much. You don't have to figure everything out tonight--just being here and talking is enough.",
    "Hey, I'm here. You don't have to explain everything perfectly or have the right words. Just tell me what it feels like--I'm listening.",
    "That sounds really painful. And honestly, it's okay that it hurts this much--what you're going through isn't small. You're allowed to feel this.",
    "You don't sound weak to me at all. You sound like someone who's been trying to hold it together for a long time. That takes a lot more strength than people realize.",
    "I'm really glad you told me. Seriously. Even if it feels messy or confusing, it matters. You matter.",
    "It's okay if nothing feels clear right now. Sometimes things just feel heavy without a clear reason. You don't have to make sense of everything immediately.",
    "That sounds like a lot to carry on your own. No wonder it feels like too much sometimes. Anyone in your position would struggle with this.",
    "I can imagine how isolating this must feel. Like no one really sees what's going on inside. But I see you trying, and that matters.",
    "You've made it through a lot already, even if it doesn't feel like it counts. The fact that you're still here, still talking, says something about you.",
    "It's okay if today just feels bad. Not every day has to be productive or meaningful. Sometimes surviving the day is enough.",
    "You don't have to hide how you feel here. You can be honest, even if it's messy or uncomfortable. I'm not going anywhere.",
    "I know it might feel like things won't change, but feelings can shift--even if it's slow and uneven. You're not stuck forever, even if it feels that way right now.",
    "I care about what you're going through. You're not just another conversation--you're someone who deserves support, understanding, and patience.",
]

SUPPORT_ONLY_RESPONSES = [
    "Hey... I'm really sorry you're feeling like this. I can't fully know what it's like for you, but I can hear how heavy it feels. You don't have to carry all of this by yourself right now--I'm here with you.",
    "That sounds really overwhelming. Like things have just been piling up and you haven't had space to breathe. I'm really glad you said something instead of keeping it all inside.",
    "I'm really sorry you're going through this. It makes sense that you'd feel exhausted if you've been dealing with so much. You don't have to figure everything out tonight--just being here and talking is enough.",
    "Hey, I'm here. You don't have to explain everything perfectly or have the right words. Just tell me what it feels like--I'm listening.",
    "That sounds really painful. And honestly, it's okay that it hurts this much--what you're going through isn't small. You're allowed to feel this.",
    "I can hear how tired you are... not just physically, but emotionally. Like everything is just weighing on you. I'm really glad you reached out instead of staying alone with it.",
    "You don't sound weak to me at all. You sound like someone who's been trying to hold it together for a long time. That takes a lot more strength than people realize.",
    "I'm really glad you told me. Seriously. Even if it feels messy or confusing, it matters. You matter.",
    "It's okay if nothing feels clear right now. Sometimes things just feel heavy without a clear reason. You don't have to make sense of everything immediately.",
    "I wish I could take some of this weight off you. Since I can't, I'll stay here with you while you talk through it. You don't have to go through this moment alone.",
    "That sounds like a lot to carry on your own. No wonder it feels like too much sometimes. Anyone in your position would struggle with this.",
    "Hey... slow down for a second. You're allowed to pause. You don't have to solve everything right now. Let's just take this one moment at a time.",
    "I can imagine how isolating this must feel. Like no one really sees what's going on inside. But I see you trying, and that matters.",
    "You've made it through a lot already, even if it doesn't feel like it counts. The fact that you're still here, still talking, says something about you.",
    "It's okay if today just feels bad. Not every day has to be productive or meaningful. Sometimes surviving the day is enough.",
    "You don't have to hide how you feel here. You can be honest, even if it's messy or uncomfortable. I'm not going anywhere.",
    "I know it might feel like things won't change, but feelings can shift--even if it's slow and uneven. You're not stuck forever, even if it feels that way right now.",
    "If it feels even a little possible, maybe think about someone you trust who could sit with you through this too. You deserve more than just carrying this alone.",
    "I care about what you're going through. You're not just another conversation--you're someone who deserves support, understanding, and patience.",
    "If things ever start to feel like too much to handle on your own, it's really important to reach out to someone nearby or a helpline. You deserve real support in those moments.",
]

_LAST_RESPONSE_BY_BUCKET: dict[str, str] = {}
_RNG = random.SystemRandom()


def get_fallback_response(label: str | None, model_available: bool) -> str:
    if not model_available:
        return _pick_response("support_only", SUPPORT_ONLY_RESPONSES)
    if label == "suicide":
        return _pick_response("high_risk", HIGH_RISK_RESPONSES)
    return _pick_response("lower_risk", LOWER_RISK_RESPONSES)


def _pick_response(bucket: str, responses: list[str]) -> str:
    last_response = _LAST_RESPONSE_BY_BUCKET.get(bucket)
    candidates = [response for response in responses if response != last_response]
    selection_pool = candidates or responses
    chosen = _RNG.choice(selection_pool)
    _LAST_RESPONSE_BY_BUCKET[bucket] = chosen
    return chosen
