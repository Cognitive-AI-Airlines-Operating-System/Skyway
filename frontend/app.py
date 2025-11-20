# frontend/app.py
import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Skyway ✈️", layout="wide")
st.title("Skyway – Smart Travel Assistant")

# ------------------------
# Flight Price Prediction
# ------------------------
st.header("✈️ Flight Price Prediction")
st.write("Enter details to predict flight price")

# Inputs
st_cols = st.columns(3)
with st_cols[0]:
    stops = st.number_input("Number of stops", min_value=0, max_value=3, value=0)
    duration_mins = st.number_input("Duration (mins)", min_value=30, value=120)
with st_cols[1]:
    days_to_dep = st.number_input("Days to departure", min_value=0, value=30)
    departure_date = st.date_input("Departure Date", value=date.today())
with st_cols[2]:
    airline = st.selectbox("Airline", ["Indigo", "Air India", "SpiceJet", "Vistara"])
    source = st.selectbox("Source", ["DEL", "HYD", "GOI", "BOM"])
    destination = st.selectbox("Destination", ["DEL", "GOI", "HYD", "BOM"])

if st.button("Predict Price"):
    # Build one-hot style payload (model might expect these columns)
    def norm_key(s: str) -> str:
        return s.replace(" ", "").replace("-", "").replace(".", "")

    onehot_payload = {
        "stops": int(stops),
        "duration_mins": int(duration_mins),
        "days_to_dep": int(days_to_dep),
        f"airline_{norm_key(airline)}": 1,
        f"source_{norm_key(source)}": 1,
        f"destination_{norm_key(destination)}": 1
    }

    # Also prepare the original payload (safe fallback)
    original_payload = {
        "airline": airline,
        "source": source,
        "destination": destination,
        "departure_date": str(departure_date),
        "stops": int(stops),
        "duration_mins": int(duration_mins),
        "days_to_dep": int(days_to_dep)
    }

    # Try one-hot first, then fallback to original_payload
    try:
        resp = requests.post(f"{API_BASE}/price/predict_price", json=onehot_payload, timeout=15)
    except Exception as e:
        st.error(f"Network error when calling price API: {e}")
        resp = None

    # If one-hot failed (non-200), try original payload
    if not resp or not resp.ok:
        try:
            resp2 = requests.post(f"{API_BASE}/price/predict_price", json=original_payload, timeout=15)
        except Exception as e:
            st.error(f"Network error when calling price API (fallback): {e}")
            resp2 = None

        if resp2 and resp2.ok:
            try:
                price = resp2.json().get("predicted_price")
                st.success(f"Predicted Price: ₹{int(price)}")
            except Exception:
                st.error(f"Unexpected response: {resp2.status_code} {resp2.text}")
        else:
            code = resp2.status_code if resp2 else "no-response"
            text = resp2.text if resp2 else ""
            st.error(f"Error fetching prediction (fallback). Status: {code}. {text}")
    else:
        try:
            price = resp.json().get("predicted_price")
            st.success(f"Predicted Price: ₹{int(price)}")
        except Exception:
            st.error(f"Unexpected response: {resp.status_code} {resp.text}")

# ------------------------
# Budget Destination Recommender
# ------------------------
st.header("🌍 Budget Destination Recommender")
st.write("Find destinations that fit your budget and preferences")

col_a, col_b = st.columns(2)
with col_a:
    budget = st.number_input("Enter budget (INR)", min_value=1000, value=20000)
    days = st.number_input("Trip days", min_value=1, value=5)
with col_b:
    # keep multiselect (more flexible) — backend accepts list of preferences
    prefs = st.multiselect("Preferences", ["beach", "culture", "adventure"], default=["culture"])

if st.button("Recommend Destinations"):
    payload = {"budget_total": float(budget), "trip_days": int(days), "preferences": prefs}
    try:
        resp = requests.post(f"{API_BASE}/destination/recommend_destinations", json=payload, timeout=20)
    except Exception as e:
        st.error(f"Network error when calling recommender API: {e}")
        resp = None

    if resp and resp.ok:
        try:
            results = resp.json()
            if results:
                # show as a table for clean view
                st.table(results)
            else:
                st.info("No destinations found for the given budget/preferences.")
        except Exception:
            st.error(f"Unexpected response format: {resp.status_code} {resp.text}")
    else:
        code = resp.status_code if resp else "no-response"
        text = resp.text if resp else ""
        st.error(f"Error calling API: {code}. {text}")

# ------------------------
# Personalized Destination Discovery (AI)
# ------------------------
st.header("🤖 Personalized Destination Discovery (AI)")
st.write("Get AI-powered travel suggestions based on your preferences")

ai_name = st.text_input("Your name", "Traveler")
ai_prefs = st.text_input("Tell the AI your preferences", "beach and culture")
ai_budget = st.number_input("Budget (INR)", min_value=500, value=3000)

# --- session state for disabling while running ---
if "ai_running" not in st.session_state:
    st.session_state.ai_running = False

if st.button("Get AI Suggestions", disabled=st.session_state.ai_running):
    # set running flag to True so button disables on next rerun
    st.session_state.ai_running = True

    payload = {"user_name": ai_name, "preferences": ai_prefs, "budget": float(ai_budget)}
    with st.spinner("Getting AI suggestions..."):
        try:
            resp = requests.post(f"{API_BASE}/ai/personalized_discovery", json=payload, timeout=30)
            if resp.ok:
                data = resp.json()
                recs = data.get("recommendations", [])
                note = data.get("note")
                cached_flag = data.get("cached", False)
                if note:
                    st.info("Server note: " + str(note))
                if cached_flag:
                    st.info("Returned from cache (fast).")
                if recs:
                    n = max(1, len(recs))
                    cols = st.columns(n)
                    for col, r in zip(cols, recs):
                        with col:
                            st.markdown(f"### {r.get('rank', '')}.")
                            st.write(r.get('text', ''))
                else:
                    st.info("No AI recommendations returned.")
            else:
                st.error(f"AI error: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Network error: {e}")
        finally:
            # reset running flag so the button becomes enabled again
            st.session_state.ai_running = False




st.title("⚡ Streamlit AI Travel Suite")

# Sidebar navigation
section = st.sidebar.selectbox(
    "Choose a tool",
    ["Chatbot", "Packing Planner", "Health Alerts", "Disruption Simulator"]
)