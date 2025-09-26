from fastapi import FastAPI

app = FastAPI(title="Skyway API")

@app.get("/health")
def health():
    return {"status": "ok"}


from app.api import reco as reco_api
app.include_router(reco_api.router, prefix="/api", tags=["recommender"])
