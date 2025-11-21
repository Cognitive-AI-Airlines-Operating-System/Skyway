from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import get_conn

router = APIRouter()

class Register(BaseModel):
    name: str
    email: str
    password: str
    home_airport: str = "HYD"

class Login(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(r: Register):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=?", (r.email,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    cur.execute("""
    INSERT INTO users (name,email,home_airport,monthly_salary,monthly_savings)
    VALUES (?,?,?,?,?)
    """, (r.name, r.email, r.home_airport, 0.0, 0.0))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"user_id": user_id}

@router.post("/login")
def login(l: Login):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name FROM users WHERE email=?", (l.email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"user_id": row["id"], "name": row["name"]}
