# backend/app/api/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..db import get_conn

# main.py likely includes this with prefix="/auth"
router = APIRouter(tags=["Auth"])

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

    # check if email already exists
    cur.execute("SELECT id FROM users WHERE email = ?", (r.email,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # insert user with password (plain text for this mini project)
    cur.execute(
        """
        INSERT INTO users (name, email, password, home_airport, monthly_salary, monthly_savings)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (r.name, r.email, r.password, r.home_airport, 0.0, 0.0),
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()

    # return data that frontend may use
    return {"user_id": user_id, "name": r.name, "email": r.email}

@router.post("/login")
def login(l: Login):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, password FROM users WHERE email = ?",
        (l.email,),
    )
    row = cur.fetchone()
    conn.close()

    # user not found OR password mismatch
    if not row or row["password"] != l.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # success – match what Streamlit expects
    return {
        "user_id": row["id"],
        "name": row["name"],
        "email": row["email"],
    }
