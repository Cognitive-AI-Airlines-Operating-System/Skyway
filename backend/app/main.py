from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import price, reco  # Make sure __init__.py exists in api/

app = FastAPI(title="Skyway API", version="1.0")

# Allow frontend to connect
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

@app.get("/health")
def health():
    return {"status": "ok"}
