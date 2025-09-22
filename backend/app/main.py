from fastapi import FastAPI
from backend.app.api import price as price_api  # <-- updated import

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flight Price API is running"}

# include the router
app.include_router(price_api.router, prefix="/api", tags=["price"])
