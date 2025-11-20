from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import get_conn


router = APIRouter()

class ProfileCreate(BaseModel):
    name: str
    email: str
    home_airport: str
    monthly_salary: float
    monthly_savings: float
    themes: str           # "beach,culture"
    usual_budget: float
    trip_length_days: int

@router.post("/create")
def create_profile(p: ProfileCreate):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name,email,home_airport,monthly_salary,monthly_savings) VALUES (?,?,?,?,?)",
        (p.name, p.email, p.home_airport, p.monthly_salary, p.monthly_savings)
    )
    user_id = cur.lastrowid

    cur.execute(
        "INSERT INTO user_preferences (user_id,themes,usual_budget,trip_length_days) VALUES (?,?,?,?)",
        (user_id, p.themes, p.usual_budget, p.trip_length_days)
    )

    conn.commit()
    conn.close()
    return {"user_id": user_id}

@router.get("/{user_id}")
def get_profile(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cur.execute("SELECT * FROM user_preferences WHERE user_id=?", (user_id,))
    prefs = cur.fetchone()
    conn.close()

    return {
        "user": dict(user),
        "preferences": dict(prefs) if prefs else None
    }
