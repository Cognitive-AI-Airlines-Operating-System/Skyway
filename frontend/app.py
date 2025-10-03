# frontend/app.py
import streamlit as st
import requests


API_BASE = "http://localhost:8000/api"


st.title("Skyway Week-1 Demo")

# Price prediction UI omitted here — reuse your Week1 UI code
st.header("Flight Price Predictor")

airline = st.selectbox("Airline", ["Indigo", "Air India", "SpiceJet", "Vistara"])
source = st.selectbox("Source", ["DEL", "HYD", "GOI", "BOM"])
destination = st.selectbox("Destination", ["DEL", "GOI", "HYD", "BOM"])
departure_date = st.date_input("Departure Date")
stops = st.number_input("Number of Stops", min_value=0, max_value=3, value=0)
duration_mins = st.number_input("Flight Duration (mins)", min_value=30, value=120)
days_to_dep = st.number_input("Days to Departure", min_value=0, value=30)

if st.button("Predict Price"):
    payload = {
        "airline": airline,
        "source": source,
        "destination": destination,
        "departure_date": str(departure_date),
        "stops": int(stops),
        "duration_mins": int(duration_mins),
        "days_to_dep": int(days_to_dep)
    }
    resp = requests.post(f"{API_BASE}/predict_price", json=payload, timeout=20)
    if resp.ok:
        price = resp.json().get("predicted_price")
        st.success(f"Estimated Price: ₹{int(price)}")
    else:
        st.error("Error calling price prediction API")


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
