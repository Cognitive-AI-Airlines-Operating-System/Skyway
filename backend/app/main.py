# backend/app/main.py
from fastapi import FastAPI
from .api import price, reco, personalized_discovery

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Skyway API", version="1.0")

# Allow frontend to connect during development
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # try initialize the heavy model; init_model logs errors but does not raise
    try:
        personalized_discovery.init_model()
    except Exception:
        pass

# Register routers
app.include_router(price.router, prefix="/price", tags=["Price Prediction"])
app.include_router(reco.router, prefix="/destination", tags=["Destination Recommender"])
app.include_router(personalized_discovery.router, prefix="/ai", tags=["Personalized AI"])

@app.get("/health")
def health():
    return {"status": "ok"}
