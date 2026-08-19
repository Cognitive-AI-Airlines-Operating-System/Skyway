# backend/app/api/profile.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..db import get_conn

# This router is registered in main.py with:
# app.include_router(profile.router, prefix="/profile", tags=["Profile"])
router = APIRouter()


class ProfileUpsert(BaseModel):
    """
    Combined model for updating a user's core profile and preferences.
    """
    user_id: int
    name: str
    email: str
    home_airport: str
    monthly_salary: float
    monthly_savings: float
    themes: str           # e.g. "beach,culture"
    usual_budget: float
    trip_length_days: int


@router.get("/{user_id}")
def get_profile(user_id: int):
    """
    Returns a FLAT profile dict by joining users + user_preferences.

    Example response:
    {
      "id": 3,
      "name": "sudheer",
      "email": "sudheer123@gmail.com",
      "home_airport": "BOM",
      "monthly_salary": 50000.0,
      "monthly_savings": 20000.0,
      "themes": "culture",
      "usual_budget": 15000.0,
      "trip_length_days": 5
    }
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
          u.id,
          u.name,
          u.email,
          u.home_airport,
          u.monthly_salary,
          u.monthly_savings,
          COALESCE(p.themes, '') AS themes,
          COALESCE(p.usual_budget, 0) AS usual_budget,
          COALESCE(p.trip_length_days, 0) AS trip_length_days
        FROM users u
        LEFT JOIN user_preferences p
          ON p.user_id = u.id
        WHERE u.id = ?
        """,
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(row)


@router.post("/create")
def upsert_profile(p: ProfileUpsert):
    """
    Updates an existing user row and inserts/updates the user_preferences row.

    It does NOT create a new user (so no UNIQUE email errors).
    This matches the Streamlit payload from the Profile page.
    """
    conn = get_conn()
    cur = conn.cursor()

    # ---- Ensure the user exists ----
    cur.execute("SELECT id FROM users WHERE id = ?", (p.user_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # ---- Update main user info ----
    cur.execute(
        """
        UPDATE users
        SET name = ?,
            email = ?,
            home_airport = ?,
            monthly_salary = ?,
            monthly_savings = ?
        WHERE id = ?
        """,
        (
            p.name,
            p.email,
            p.home_airport,
            p.monthly_salary,
            p.monthly_savings,
            p.user_id,
        ),
    )

    # ---- Upsert user_preferences ----
    cur.execute(
        "SELECT id FROM user_preferences WHERE user_id = ?",
        (p.user_id,),
    )
    existing_pref = cur.fetchone()

    if existing_pref:
        # Update existing preference record
        cur.execute(
            """
            UPDATE user_preferences
            SET themes = ?,
                usual_budget = ?,
                trip_length_days = ?
            WHERE user_id = ?
            """,
            (p.themes, p.usual_budget, p.trip_length_days, p.user_id),
        )
    else:
        # Insert new preference record
        cur.execute(
            """
            INSERT INTO user_preferences (user_id, themes, usual_budget, trip_length_days)
            VALUES (?, ?, ?, ?)
            """,
            (p.user_id, p.themes, p.usual_budget, p.trip_length_days),
        )

    conn.commit()
    conn.close()

    return {"detail": "Profile updated"}
