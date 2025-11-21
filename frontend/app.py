# frontend/app.py
import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Skyway ✈️", layout="wide")

st.sidebar.title("Skyway Menu")
page = st.sidebar.selectbox("Go to", [
    "Home",
    "Flights",
    "Destinations",
    "AI Tools",
    "Group Travel",
    "Profile",
])

# Then wrap your existing UI:
st.title("Skyway – Cognitive AI Airline OS")

if page == "Home":
    st.subheader("Welcome to Skyway")
    st.write("Use the sidebar to explore features.")


elif page == "Flights":
  # move flight price + carbon + disruptions UI here
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



 # --- Carbon Footprint ---
st.markdown("### 🌍 Carbon Footprint")
distance = st.number_input("Flight Distance (km):", min_value=1)
passengers = st.number_input("Number of Passengers:", min_value=1, step=1)

if st.button("Calculate Carbon"):
    payload = {"distance_km": distance, "passengers": passengers}
    response = requests.post(f"{API_BASE}/flights/carbon", json=payload)
    if response.status_code == 200:
        data = response.json()
        st.success("Carbon Footprint Result")
        st.write(f"Distance: {data['distance']} km")
        st.write(f"Passengers: {data['passengers']}")
        st.write(f"Carbon Emissions: {data['emissions']} kg CO₂")
    else:
        st.error(response.json())
            

# --- Disruption Simulator ---
st.markdown("### ⚠️ Disruption Simulator")
airline_d = st.text_input("Airline (for disruption):")
source_d = st.text_input("Source Airport Code (Disruption):")
destination_d = st.text_input("Destination Airport Code (Disruption):")
departure_time_d = st.text_input("Departure Time (YYYY-MM-DDTHH:MM:SS):")

if st.button("Simulate Disruption"):
    payload = {
        "airline": airline_d,
        "source": source_d,
        "destination": destination_d,
        "departure_time": departure_time_d
    }
    response = requests.post(f"{API_BASE}/disruptions/simulate", json=payload)
    if response.status_code == 200:
        data = response.json()
        st.success("Disruption Simulation Result")
        st.write(f"Airline: {data['airline']}")
        st.write(f"Route: {data['source']} → {data['destination']}")
        st.write(f"Status: **{data['status']}**")
        if data["status"] == "delayed":
            st.write(f"Delay: {data['delay_mins']} minutes")
        st.write(f"Reason: {data['reason']}")
    else:
        st.error(response.json())



elif page == "Destinations":
# move budget recommendation + AI discovery UI here
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




elif page == "AI Tools":
    # move chatbot + itinerary + packing + health + savings UI here
    st.header(" ⚡ AI Tools")

    # Chatbot
    st.subheader("Chatbot")
    user_message = st.text_input("Enter your message:")
    if st.button("Send to Chatbot"):
        payload = {"message": user_message}
        response = requests.post(f"{API_BASE}/chatbot", json=payload)
        st.write("Response:", response.json())


    # Itinerary
    st.subheader("Travel Itinerary")
    destination = st.text_input("Destination:")
    days = st.number_input("Number of days:", min_value=1, step=1)
    if st.button("Generate Itinerary"):
        payload = {"destination": destination, "days": days}
        response = requests.post(f"{API_BASE}/itinerary", json=payload)
        st.json(response.json())               # show structured output


    # Packing
    st.subheader("Packing Suggestions")
    trip_type = st.selectbox("Trip Type:", ["Business", "Vacation", "Adventure"])
    if st.button("Get Packing List"):
        payload = {"trip_type": trip_type}
        response = requests.post(f"{API_BASE}/packing", json=payload)
        st.json(response.json())


    # Health
    st.subheader("Health Tips")
    location = st.text_input("Travel Location:")
    if st.button("Get Health Advice"):
        payload = {"location": location}
        response = requests.post(f"{API_BASE}/health", json=payload)
        st.json(response.json())


    # Savings
    st.subheader("Savings Calculator")
    budget = st.number_input("Budget ($):", min_value=0)
    duration = st.number_input("Duration (days):", min_value=1)
    if st.button("Calculate Savings"):
        payload = {"budget": budget, "duration": duration}
        response = requests.post(f"{API_BASE}/savings", json=payload)
        st.json(response.json())



# elif page == "Group Travel":
#     # simple forms to call /groups APIs

# elif page == "Profile":
#     # call /profile APIs



#  st.title("⚡ Streamlit AI Travel Suite")

# # Sidebar navigation
# section = st.sidebar.selectbox(
#     "Choose a tool",
#     ["Chatbot", "Packing Planner", "Health Alerts", "Disruption Simulator"]
# )


