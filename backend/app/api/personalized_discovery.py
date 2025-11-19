# backend/app/api/personalized_discovery.py
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import logging
import sys
import os
import requests
import re
import time
from typing import Any

# --- logging: INFO for normal use ---
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
router = APIRouter()
logger = logging.getLogger(__name__)

# ---- Simple in-memory TTL cache (keyed by user_name|prefs|budget) ----
_AI_CACHE: dict[str, tuple[float, Any]] = {}  # key -> (expiry_timestamp, value)
CACHE_TTL_SECONDS = 120  # cache TTL in seconds (2 minutes)

def cache_get(key: str):
    entry = _AI_CACHE.get(key)
    if not entry:
        return None
    expiry, val = entry
    if time.time() > expiry:
        _AI_CACHE.pop(key, None)
        return None
    return val

def cache_set(key: str, value: Any, ttl: int = CACHE_TTL_SECONDS):
    _AI_CACHE[key] = (time.time() + ttl, value)

# ---- API setup ----
class DiscoveryRequest(BaseModel):
    user_name: str | None = "Traveler"
    preferences: str | None = "beach and culture"
    budget: float | None = 2000

# Model globals
generator = None
MODEL_NAME = "google/flan-t5-small"

# Optional HuggingFace Inference API fallback (only used if HF_API_TOKEN env var set)
HF_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "google/flan-t5-small"

def hf_inference(prompt: str) -> str:
    if not HF_TOKEN:
        return ""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 140, "temperature": 0.7, "top_p": 0.9},
    }
    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30,
        )
        if r.ok:
            out = r.json()
            if isinstance(out, list) and len(out) > 0 and "generated_text" in out[0]:
                return out[0]["generated_text"].strip()
            if isinstance(out, dict) and "error" in out:
                logger.warning("HF API error: %s", out["error"])
        else:
            logger.warning("HF API request failed: %s %s", r.status_code, r.text)
    except Exception as e:
        logger.exception("HF inference call failed: %s", e)
    return ""

# --- init_model: called from FastAPI startup ---
def init_model():
    """
    Initialize the transformers pipeline into global `generator`.
    Safe to call multiple times.
    Returns True if model loaded, False otherwise.
    """
    global generator
    if generator is not None:
        return True
    try:
        from transformers import pipeline
        # text2text (flan-t5) on CPU
        generator = pipeline("text2text-generation", model=MODEL_NAME, device=-1)
        logger.info("Model loaded by init_model(): %s", MODEL_NAME)
        return True
    except Exception as e:
        logger.exception("init_model() failed (model not loaded): %s", e)
        generator = None
        return False

# --- Simple per-IP rate limiter (in-memory; single-process demo only) ---
_RATE_WINDOW = 60    # seconds
_RATE_LIMIT = 10     # requests per window per IP
_IP_USAGE: dict[str, tuple[float, int]] = {}  # ip -> (window_start, count)

def rate_limit_dep(request: Request):
    ip = request.client.host or "unknown"
    now = time.time()
    window_start, count = _IP_USAGE.get(ip, (now, 0))
    if now - window_start > _RATE_WINDOW:
        _IP_USAGE[ip] = (now, 1)
    else:
        if count >= _RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests - slow down")
        _IP_USAGE[ip] = (window_start, count + 1)

# Router endpoint with rate-limit dependency
@router.post("/personalized_discovery", dependencies=[Depends(rate_limit_dep)])
def discover(req: DiscoveryRequest):
    user_name = req.user_name or "Traveler"
    prefs = req.preferences or "travel"
    budget = int(req.budget or 2000)

    # cache key
    cache_key = f"{user_name}|{prefs}|{budget}"
    cached = cache_get(cache_key)
    if cached:
        logger.info("Returning cached AI result for key=%s", cache_key)
        # mark cached True before returning
        cached_copy = dict(cached)
        cached_copy["cached"] = True
        return cached_copy

    # One-shot example to teach the model format
    example = (
        "Example output (this is an example showing the required format):\n"
        "1. Goa — golden beaches and budget-friendly shacks.\n"
        "2. Pondicherry — calm French Quarter and seaside promenades.\n"
        "3. Gokarna — peaceful beaches ideal for low-budget travelers.\n\n"
    )

    prompt = (
        example
        + f"Now, for a traveler named {user_name} who likes {prefs} with a budget of {budget} INR, "
        "provide EXACTLY 3 numbered lines in the same format as the example (no extra commentary):\n1."
    )

    source = "none"
    text = ""

    # If generator not available locally, try HF API or fallback
    if generator is None:
        source = "hf_api" if HF_TOKEN else "fallback"
        if HF_TOKEN:
            text = hf_inference(prompt)
        if not text:
            # deterministic fallback suggestions
            fallback = [
                {"rank": 1, "text": f"Goa — sandy beaches and budget stays suitable for ~{budget} INR."},
                {"rank": 2, "text": f"Pondicherry — relaxed French Quarter + calm beaches for a mellow getaway."},
                {"rank": 3, "text": f"Rishikesh — adventure + riverside stays, good for budget travelers."},
            ]
            result = {"recommendations": fallback, "note": "model_unavailable_fallback", "cached": False}
            cache_set(cache_key, result)
            # save fallback sample
            try:
                backend_dir = Path(__file__).resolve().parents[2]
                sample_dir = backend_dir / "notebooks"
                sample_dir.mkdir(parents=True, exist_ok=True)
                sample_file = sample_dir / "ai_samples.txt"
                with open(sample_file, "a", encoding="utf-8") as f:
                    f.write(f"---\nSource: fallback\nPrompt: {prompt}\nOutput (fallback):\n")
                    for item in fallback:
                        f.write(f"{item['rank']}. {item['text']}\n")
                    f.write("\n")
                logger.info("AI fallback sample saved to: %s", sample_file)
            except Exception as e:
                logger.exception("Failed to save fallback AI sample: %s", e)
            return result

    else:
        source = "local"
        # Try sampled generation first with milder randomness, anti-repetition controls
        try:
            out = generator(
                prompt,
                max_new_tokens=140,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_p=0.90,
                repetition_penalty=1.15,
                no_repeat_ngram_size=3,
            )
            logger.info("Generation raw output (sampled): %s", bool(out and len(out) and out[0].get("generated_text")))
            text = (out[0].get("generated_text") or "").strip()
            source = "local_sampled"
        except Exception as e:
            logger.exception("Generation error (sampled): %s", e)
            text = ""

        # deterministic retry if sampled returned nothing
        if not text:
            try:
                out2 = generator(prompt, max_new_tokens=80, do_sample=False, num_return_sequences=1)
                logger.info("Generation raw output (deterministic retry): %s", bool(out2 and len(out2) and out2[0].get("generated_text")))
                text = (out2[0].get("generated_text") or "").strip()
                source = "local_deterministic"
            except Exception as e:
                logger.exception("Generation error (deterministic retry): %s", e)
                text = ""

        # If still empty and HF available, try HF as fallback
        if not text and HF_TOKEN:
            logger.warning("Local model empty; trying Hugging Face Inference API fallback.")
            text = hf_inference(prompt) or ""
            if text:
                source = "hf_api"

        # If still empty, fallback deterministic suggestions (and save)
        if not text:
            logger.warning("Model returned empty text after retries; using fallback.")
            fallback = [
                {"rank": 1, "text": f"Goa — sandy beaches and budget stays suitable for ~{budget} INR."},
                {"rank": 2, "text": f"Pondicherry — relaxed French Quarter + calm beaches for a mellow getaway."},
                {"rank": 3, "text": f"Rishikesh — adventure + riverside stays, good for budget travelers."},
            ]
            result = {"recommendations": fallback, "note": "model_empty_fallback", "cached": False}
            cache_set(cache_key, result)
            try:
                backend_dir = Path(__file__).resolve().parents[2]
                sample_dir = backend_dir / "notebooks"
                sample_dir.mkdir(parents=True, exist_ok=True)
                sample_file = sample_dir / "ai_samples.txt"
                with open(sample_file, "a", encoding="utf-8") as f:
                    f.write(f"---\nSource: fallback\nPrompt: {prompt}\nOutput (fallback due to empty model output):\n")
                    for item in fallback:
                        f.write(f"{item['rank']}. {item['text']}\n")
                    f.write("\n")
                logger.info("Saved fallback AI sample to: %s", sample_file)
            except Exception:
                logger.exception("Failed to save fallback AI sample")
            return result

    # --- Post-processing & de-duplication ---
    if text.startswith(example):
        text = text[len(example):].strip()

    text_norm = " ".join(text.split())
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    if len(lines) == 1:
        numbered_split = re.split(r'\s*\d[\.\)]\s*', text_norm)
        numbered_split = [s.strip() for s in numbered_split if s.strip()]
        if len(numbered_split) >= 3:
            lines = numbered_split
        else:
            parts = re.split(r'\s+[–—-]\s+|\s*;+\s*|\s*\.\s*', text_norm)
            parts = [p.strip() for p in parts if p.strip()]
            dedup = []
            for p in parts:
                if not dedup or p != dedup[-1]:
                    dedup.append(p)
            if len(dedup) >= 3:
                lines = dedup
            else:
                city_candidates = re.findall(r'\b([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*)\b', text_norm)
                seen_cities = []
                for c in city_candidates:
                    if c.lower() not in [s.lower() for s in seen_cities]:
                        seen_cities.append(c)
                    if len(seen_cities) >= 3:
                        break
                if seen_cities:
                    lines = [f"{c} — recommended for {prefs}" for c in seen_cities]

    lines = [l for l in lines if l]
    seen_set = set()
    unique_lines = []
    for l in lines:
        key = l.lower()
        if key not in seen_set:
            unique_lines.append(l)
            seen_set.add(key)
    unique_lines = unique_lines[:3]

    if len(unique_lines) < 3:
        pad = [
            f"Goa — sandy beaches and budget stays suitable for ~{budget} INR.",
            f"Pondicherry — relaxed French Quarter + calm beaches for a mellow getaway.",
            f"Rishikesh — adventure + riverside stays, good for budget travelers.",
        ]
        for p in pad:
            if len(unique_lines) >= 3:
                break
            if p.lower() not in [u.lower() for u in unique_lines]:
                unique_lines.append(p)

    recs = []
    for i, line in enumerate(unique_lines, start=1):
        cleaned = line.lstrip("0123456789. )\t")
        recs.append({"rank": i, "text": cleaned})

    result = {"recommendations": recs, "note": f"source:{source}", "cached": False}
    cache_set(cache_key, result)

    # Save sample
    try:
        backend_dir = Path(__file__).resolve().parents[2]
        sample_dir = backend_dir / "notebooks"
        sample_dir.mkdir(parents=True, exist_ok=True)
        sample_file = sample_dir / "ai_samples.txt"
        with open(sample_file, "a", encoding="utf-8") as f:
            f.write(f"---\nSource: {source}\nPrompt: {prompt}\nOutput:\n{text}\n\n")
        logger.info("AI sample saved to: %s", sample_file)
    except Exception as e:
        logger.exception("Could not write ai sample: %s", e)

    return result
