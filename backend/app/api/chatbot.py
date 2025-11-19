from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

generator = pipeline("text-generation", model="distilgpt2")

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    prompt = f"Travel assistant:\nUser: {req.message}\nAssistant:"
    out = generator(prompt, max_length=80, num_return_sequences=1)
    text = out[0]["generated_text"]
    reply = text.replace(prompt, "").strip()
    return {"reply": reply}
