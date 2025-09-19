from fastapi import FastAPI

app = FastAPI(title="Skyway API")

@app.get("/health")
def health():
    return {"status": "ok"}

