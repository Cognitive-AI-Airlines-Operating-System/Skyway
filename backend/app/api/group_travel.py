# backend/app/api/group_travel.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..db import get_conn  # ✅ fixed: relative import

router = APIRouter()

class GroupCreate(BaseModel):
    name: str
    trip_city: str
    trip_start_date: str
    trip_end_date: str
    owner_user_id: int

@router.post("/create")
def create_group(g: GroupCreate):
    conn = get_conn()
    cur = conn.cursor()

    # Insert into groups table
    cur.execute("""
    INSERT INTO groups (name, trip_city, trip_start_date, trip_end_date, owner_user_id)
    VALUES (?,?,?,?,?)
    """, (g.name, g.trip_city, g.trip_start_date, g.trip_end_date, g.owner_user_id))
    group_id = cur.lastrowid

    # Insert owner as member
    cur.execute("""
    INSERT INTO group_members (group_id, user_id, role)
    VALUES (?,?,?)
    """, (group_id, g.owner_user_id, "owner"))

    conn.commit()
    conn.close()
    return {"group_id": group_id}


class AddMember(BaseModel):
    group_id: int
    user_id: int
    role: str = "member"

@router.post("/add_member")
def add_member(m: AddMember):
    conn = get_conn()
    cur = conn.cursor()

    # Check group exists
    cur.execute("SELECT id FROM groups WHERE id=?", (m.group_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Group not found")

    # Insert new member
    cur.execute("""
    INSERT INTO group_members (group_id, user_id, role)
    VALUES (?,?,?)
    """, (m.group_id, m.user_id, m.role))

    conn.commit()
    conn.close()
    return {"status": "added"}


@router.get("/{group_id}")
def get_group(group_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM groups WHERE id=?", (group_id,))
    group = cur.fetchone()
    if not group:
        conn.close()
        raise HTTPException(status_code=404, detail="Group not found")

    cur.execute("SELECT * FROM group_members WHERE group_id=?", (group_id,))
    members = [dict(row) for row in cur.fetchall()]

    conn.close()
    return {"group": dict(group), "members": members}
