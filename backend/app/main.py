from fastapi import FastAPI

app = FastAPI(title="Cognitive AI Airlines - API")

@app.get("/health")
def health():
    return {"status": "ok"}
