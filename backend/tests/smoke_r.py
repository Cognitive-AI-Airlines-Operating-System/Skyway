# backend/tests/smoke_r.py
import requests

BASE = "http://127.0.0.1:8000"

def test_optimized_route():
    payload = {
        "source": "HYD",
        "destination": "DEL",
        "optimize_for": "price"
    }
    resp = requests.post(f"{BASE}/ai/optimized_route", json=payload, timeout=10)
    print("Status /ai/optimized_route:", resp.status_code)
    print(resp.json())

def test_group_flow():
    # 1. Create group
    create_payload = {
        "name": "Test Group R",
        "trip_city": "Goa",
        "trip_start_date": "2025-12-20",
        "trip_end_date": "2025-12-25",
        "owner_user_id": 1
    }
    resp = requests.post(f"{BASE}/groups/create", json=create_payload, timeout=10)
    print("Status /groups/create:", resp.status_code)
    data = resp.json()
    print(data)
    group_id = data["group_id"]

    # 2. Add member
    member_payload = {
        "group_id": group_id,
        "user_id": 2,
        "role": "member"
    }
    resp = requests.post(f"{BASE}/groups/add_member", json=member_payload, timeout=10)
    print("Status /groups/add_member:", resp.status_code)
    print(resp.json())

    # 3. Get group
    resp = requests.get(f"{BASE}/groups/{group_id}", timeout=10)
    print(f"Status /groups/{group_id}:", resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    test_optimized_route()
    test_group_flow()
