# frontend/app.py
import streamlit as st
import requests


API_BASE = "http://localhost:8000/api"


st.title("Skyway Week-1 Demo")

# Price prediction UI omitted here — reuse your Week1 UI code

st.header("Destination Recommender")
budget = st.number_input("Budget (₹)", min_value=1000, value=20000)
days = st.number_input("Trip days", min_value=1, value=5)
prefs = st.multiselect("Preferences", ["beach","culture","adventure"], default=["culture"])



if st.button("Recommend"):
    payload = {"budget_total": float(budget), "trip_days": int(days), "preferences": prefs}
    resp = requests.post(f"{API_BASE}/recommend_destinations", json=payload, timeout=20)
    if resp.ok:
        for i, r in enumerate(resp.json(),1):
            st.write(f"{i}. **{r['city']}**, cost: ₹{int(r['trip_cost'])}, best months: {r['best_months']}")
    else:
        st.error("Error calling API")
