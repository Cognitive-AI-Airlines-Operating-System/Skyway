# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api import price, reco, personalized_discovery, chatbot
from .api import packing


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
    lifespan=lifespan
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
app.include_router(chatbot.router, prefix="/assistant", tags=["Chatbot"])  # ✅ new router added
app.include_router(packing.router, prefix="/planner", tags=["Packing"])


@app.get("/health")
def health():
    return {"status": "ok"}
