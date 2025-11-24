# backend/app/api/chatbot.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

def simple_travel_bot(user_msg: str) -> str:
    msg = user_msg.lower()

    # very simple examples – you can expand later
    if "ooty" in msg and "shimla" in msg:
        return (
            "Both Ooty and Shimla are great!\n\n"
            "- **Ooty**: Better in summer, tea gardens, gentler hills, good if you are in South India.\n"
            "- **Shimla**: Better if you want colder weather, colonial vibe, snowfall in winter.\n\n"
            "If you’re in South India and want a shorter, cheaper trip → Ooty.\n"
            "If you want snow / classic hill-station feel and don’t mind travel time → Shimla."
        )

    if "best time" in msg or "which month" in msg:
        return (
            "For most Indian hill stations:\n"
            "- **March–June**: Pleasant, peak tourist season.\n"
            "- **July–September**: Monsoon, green but risk of landslides.\n"
            "- **October–February**: Colder, good for off-season travel and snow in the north.\n\n"
            "Tell me the city and month, and I’ll give more specific tips."
        )

    if "delhi" in msg and "march" in msg:
        return (
            "Delhi in March is usually pleasant (20–30°C).\n"
            "- Good for sightseeing: India Gate, Qutub Minar, Red Fort, Chandni Chowk.\n"
            "- Carry light cotton clothes + a light jacket for evenings.\n"
            "- Air quality can vary, so a basic mask is still a good idea."
        )

    # default fallback
    return (
        "I’m a simple travel helper bot for Skyway 😄.\n"
        "Ask me things like:\n"
        "- 'Ooty or Shimla in January?'\n"
        "- 'Is March good for visiting Delhi?'\n"
        "- 'What to pack for a 3-day trip to Goa in May?'\n"
        "I’ll try to give practical suggestions."
    )

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    reply = simple_travel_bot(req.message)
    return ChatResponse(reply=reply)
