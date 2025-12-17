import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def _clean_ai_text(text: str) -> str | None:
    """Return cleaned platform-style text, or None if it smells like 'AI voice'."""
    if not text:
        return None

    cleaned = text.strip()

    # Remove surrounding quotes if model returns them
    cleaned = cleaned.strip('"').strip("'").strip()

    # Kill common assistant-y openers
    lowered = cleaned.lower()
    banned_prefixes = (
        "i can",
        "i will",
        "as an ai",
        "as a language model",
        "here is",
        "sure",
        "based on the provided",
        "based on the information",
        "the provided data",
        "of course",
    )
    if lowered.startswith(banned_prefixes):
        return None

    # Remove any leftover "AI disclaimers" lines
    cleaned = re.sub(r"(?im)^(as an ai.*)$", "", cleaned).strip()
    cleaned = re.sub(r"(?im)^(i (can|cannot|can't).*)$", "", cleaned).strip()

    # Keep it short-ish (prevents rambly essays)
    # If it’s too long, keep first 3 sentences.
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    if len(sentences) > 3:
        cleaned = " ".join(sentences[:3]).strip()

    return cleaned if cleaned else None


def _ollama_generate(prompt: str, timeout: float = 15.0) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def generate_parcel_summary(parcel) -> str:
    prompt = f"""
You are writing copy for a land intelligence platform.

STRICT RULES:
- Do NOT mention yourself, AI, models, or "provided data"
- Do NOT use first person ("I", "we")
- Output ONLY the final text (no preamble)
- Neutral, professional tone
- 2 sentences max
- No legal or financial advice

Parcel:
Canton: {parcel.canton}
Area: {round(parcel.area_m2, 2)} m²
Zoning: {parcel.zoning}
Buildable: {parcel.is_buildable}
"""

    try:
        raw = _ollama_generate(prompt, timeout=12.0)
        cleaned = _clean_ai_text(raw)
        if cleaned:
            return cleaned
    except Exception as e:
        print("AI summary error:", e)

    # Fallback (guaranteed clean)
    return (
        f"Parcel in canton {parcel.canton} with an area of {round(parcel.area_m2, 2)} m² "
        f"and zoning '{parcel.zoning}'. Buildable status: {parcel.is_buildable}."
    )


def generate_development_potential(parcel, base_potential: str) -> str | None:
    prompt = f"""
You are writing copy for a land intelligence platform.

STRICT RULES:
- Do NOT mention yourself, AI, models, or "provided data"
- Do NOT use first person ("I", "we")
- Output ONLY the final text (no preamble)
- Neutral, realistic tone (no hype)
- Maximum 3 sentences
- No legal or financial advice
- Do not invent facts (no transport proximity, no comps, no market claims)

Parcel:
Canton: {parcel.canton}
Area: {round(parcel.area_m2, 2)} m²
Zoning: {parcel.zoning}
Buildable: {parcel.is_buildable}
Classified potential: {base_potential}

Write a short development potential note that states:
1) what types of development may be plausible (generic)
2) one key uncertainty to verify with the canton
"""

    try:
        raw = _ollama_generate(prompt, timeout=12.0)
        cleaned = _clean_ai_text(raw)
        return cleaned  # can be None if it fails the filter
    except Exception as e:
        print("AI development potential error:", e)
        return None
