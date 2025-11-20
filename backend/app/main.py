# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ✅ use relative imports from the same package (backend.app)
from .api import (
    price,
    reco,
    personalized_discovery,
    chatbot,
    profile,       # Block P – Profile router
    itinerary,     # Itinerary router
    carbon,        # ✅ NEW Carbon router imported here
)


# lifespan context manager replaces deprecated startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        personalized_discovery.init_model()
    except Exception:
        # init_model logs errors but does not raise
        pass
    yield
    # Shutdown logic (optional)
    # e.g., close DB connections, cleanup resources


app = FastAPI(
    title="Skyway API",
    version="1.0",
    lifespan=lifespan,
)

# Allow frontend to connect during development
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(price.router, prefix="/price", tags=["Price Prediction"])
app.include_router(reco.router, prefix="/destination", tags=["Destination Recommender"])
app.include_router(personalized_discovery.router, prefix="/ai", tags=["Personalized AI"])
app.include_router(chatbot.router, prefix="/assistant", tags=["Chatbot"])
app.include_router(itinerary.router, prefix="/ai", tags=["Itinerary"])

# 🧱 Block P routers
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(carbon.router, prefix="/ai", tags=["Carbon"])   # ✅ NEW Carbon endpoint added


@app.get("/health")
def health():
    return {"status": "ok"}
