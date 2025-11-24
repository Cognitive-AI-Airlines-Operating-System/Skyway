# frontend/app.py
import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

# ---------- SESSION STATE ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Skyway ✈️",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- GLOBAL STYLES ----------
CUSTOM_CSS = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Sidebar (no nav inside now) */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050b18 0%, #020814 100%);
    color: #ffffff;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Top bar */
.top-bar {
    background: #020814;
    color: #f5f5f5;
    padding: 0.35rem 3rem;
    font-size: 0.78rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Brand bar */
.brand-bar {
    background: #071227;
    color: #ffffff;
    padding: 0.7rem 3rem 0.5rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-bar-logo {
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: 0.16em;
}
.brand-bar-logo span {
    font-size: 1rem;
    font-weight: 500;
    margin-left: 0.55rem;
}

/* Top navigation (radio in main area) */
.nav-container {
    background: #050b18;
    padding: 0.45rem 3rem 0.1rem 3rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
div[data-testid="stRadio"] > label {
    display: none;
}
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex;
    gap: 1.5rem;
    justify-content: flex-end;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    padding: 0.1rem 0.2rem;
    font-size: 0.96rem;
    cursor: pointer;
    opacity: 0.68;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-baseweb="radio"] {
    padding-bottom: 0.4rem;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label span:nth-child(1) {
    display: none; /* hide the radio dot */
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label span:nth-child(2) {
    border-bottom: 2px solid transparent;
    padding-bottom: 0.1rem;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] {
    opacity: 1;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] span:nth-child(2) {
    border-color: #ffffff;
}

/* Hero area */
.hero {
    position: relative;
    margin: 0 -3rem 2rem -3rem;
    padding: 2.6rem 3rem 3.1rem 3rem;
    background-image:
      linear-gradient(120deg, rgba(5,10,25,0.82), rgba(5,10,25,0.15)),
      url("https://images.pexels.com/photos/358220/pexels-photo-358220.jpeg?auto=compress&cs=tinysrgb&w=1600");
    background-size: cover;
    background-position: center;
    border-radius: 0 0 28px 28px;
    color: #ffffff;
    box-shadow: 0 18px 40px rgba(0,0,0,0.45);
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 0.32rem 0.9rem;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    background: rgba(255,255,255,0.16);
    margin-bottom: 0.9rem;
}
.hero-left-title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.hero-left-subtitle {
    font-size: 1.0rem;
    opacity: 0.9;
    max-width: 520px;
    margin-bottom: 1.4rem;
}
.hero-stat-row {
    display: flex;
    gap: 1.8rem;
    margin-top: 1.1rem;
}
.hero-stat {
    font-size: 0.86rem;
}
.hero-stat strong {
    display: block;
    font-size: 1.08rem;
}

/* Hero login/register card */
.hero-card {
    background: rgba(5, 10, 25, 0.92);
    padding: 1.4rem 1.5rem 1.1rem 1.5rem;
    border-radius: 18px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
    backdrop-filter: blur(8px);
}

/* Buttons */
div.stButton > button {
    border-radius: 999px;
    border: none;
    padding: 0.45rem 1.4rem;
    font-weight: 600;
    font-size: 0.9rem;
    background: linear-gradient(135deg, #ffb347, #ff5f6d);
    color: #050b18;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}
div.stButton > button:hover {
    filter: brightness(1.06);
}

/* Inputs */
input, select, textarea {
    border-radius: 999px !important;
}

/* Metrics row */
.metrics-row {
    display: flex;
    gap: 1.4rem;
    margin: 0.8rem 0 1.2rem 0;
}
.metrics-pill {
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    background: #050b18;
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 0.86rem;
}
.metrics-pill-label {
    opacity: 0.7;
    font-size: 0.8rem;
}
.metrics-pill-value {
    font-weight: 600;
    font-size: 0.98rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- HELPERS ----------
def require_login():
    if not st.session_state.user_id:
        st.warning("Please login on the Home page to use this section.")
        st.stop()


def top_bars():
    """Contact strip + brand bar (with only flight emoji)."""
    st.markdown(
        """
        <div class="top-bar">
            <div>📞 +91xxxxxxxxxx &nbsp;&nbsp; | &nbsp;&nbsp; ✉️ xxxxx@gmail.com</div>
            <div>Hyderabad, Banjara Hills</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="brand-bar">
            <div class="brand-bar-logo">
                ✈ <span>Skyway Cognitive Airline OS</span>
            </div>
            <div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- SIDEBAR (just status) ----------
st.sidebar.title("Skyway")
if st.session_state.user_id:
    st.sidebar.success(f"Logged in as **{st.session_state.user_name}**")
else:
    st.sidebar.info("Login from the Home page to unlock all tools.")

# ---------- HEADER + NAV ----------
top_bars()

with st.container():
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    if "nav" not in st.session_state:
        st.session_state.nav = "Home"

    page = st.radio(
        "Navigation",
        ["Home", "Flights", "Destinations", "AI Tools", "Group Travel", "Profile"],
        index=["Home", "Flights", "Destinations", "AI Tools", "Group Travel", "Profile"].index(
            st.session_state.nav
        ),
        horizontal=True,
        key="nav",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================
# HOME PAGE
# ==================================
if page == "Home":
    with st.container():
        st.markdown('<div class="hero">', unsafe_allow_html=True)

        col_left, col_right = st.columns([2.1, 1])

        with col_left:
            st.markdown(
                '<div class="hero-pill">AI-POWERED AIRLINE OPERATING SYSTEM</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="hero-left-title">Fly smarter, not harder.</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="hero-left-subtitle">'
                'Plan trips, predict fares, optimize carbon footprint and manage group journeys in one AI-first workspace.'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <ul style="margin-left:1rem; font-size:0.95rem;">
                    <li>🔮 Flight price prediction with ML</li>
                    <li>🌍 Budget-based destination discovery</li>
                    <li>🤖 AI travel assistant, packing & health advice</li>
                    <li>👥 Group travel & smart savings planner</li>
                </ul>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div class="hero-stat-row">
                    <div class="hero-stat">
                        <strong>10K+</strong>
                        Trips simulated
                    </div>
                    <div class="hero-stat">
                        <strong>25%</strong>
                        Avg. cost savings
                    </div>
                    <div class="hero-stat">
                        <strong>CO₂ Smart</strong>
                        Carbon-optimized routes
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown('<div class="hero-card">', unsafe_allow_html=True)
            st.markdown(
                "<h4>Login or create an account</h4>"
                "<small>Sync your profile, preferences and trips.</small>",
                unsafe_allow_html=True,
            )

            login_tab, register_tab = st.tabs(["🔐 Login", "🆕 Register"])

            # LOGIN
            with login_tab:
                with st.form("login_form"):
                    login_email = st.text_input("Email", key="login_email")
                    login_password = st.text_input(
                        "Password", type="password", key="login_password"
                    )
                    login_submit = st.form_submit_button("Login")

                if login_submit:
                    payload = {"email": login_email, "password": login_password}
                    try:
                        resp = requests.post(
                            f"{API_BASE}/auth/login", json=payload, timeout=15
                        )
                    except Exception as e:
                        st.error(f"Network error during login: {e}")
                    else:
                        if resp.status_code == 200:
                            try:
                                data = resp.json()
                                st.session_state.user_id = data["user_id"]
                                st.session_state.user_name = data["name"]
                                st.success(f"Logged in as {data['name']}")
                            except Exception:
                                st.error(
                                    "Login succeeded but response was not JSON. "
                                    f"Status {resp.status_code}, body: {resp.text}"
                                )
                        else:
                            try:
                                detail = resp.json().get("detail", "Login failed")
                            except Exception:
                                detail = (
                                    f"Login failed. Status {resp.status_code}, body: {resp.text}"
                                )
                            st.error(detail)

            # REGISTER
            with register_tab:
                with st.form("register_form"):
                    reg_name = st.text_input("Full Name", key="reg_name")
                    reg_email = st.text_input("Email", key="reg_email")
                    reg_password = st.text_input(
                        "Password", type="password", key="reg_password"
                    )
                    reg_home_airport = st.text_input(
                        "Home Airport", value="HYD", key="reg_home_airport"
                    )
                    register_submit = st.form_submit_button("Create account")

                if register_submit:
                    payload = {
                        "name": reg_name,
                        "email": reg_email,
                        "password": reg_password,
                        "home_airport": reg_home_airport,
                    }
                    try:
                        resp = requests.post(
                            f"{API_BASE}/auth/register", json=payload, timeout=15
                        )
                    except Exception as e:
                        st.error(f"Network error during registration: {e}")
                    else:
                        if resp.status_code in (200, 201):
                            st.success(
                                "Registered successfully! You can now login from the Login tab."
                            )
                        else:
                            try:
                                detail = resp.json().get("detail", "Registration failed")
                            except Exception:
                                detail = (
                                    f"Registration failed. "
                                    f"Status {resp.status_code}, body: {resp.text}"
                                )
                            st.error(detail)

            st.markdown("</div>", unsafe_allow_html=True)  # hero-card

        st.markdown("</div>", unsafe_allow_html=True)  # hero

    # Feature metrics row
    st.markdown(
        """
        <div class="metrics-row">
            <div class="metrics-pill">
                <span class="metrics-pill-label">Core Engine</span>
                <span class="metrics-pill-value">Flights & Carbon Tools</span>
            </div>
            <div class="metrics-pill">
                <span class="metrics-pill-label">Personalization</span>
                <span class="metrics-pill-value">Profiles & AI Destinations</span>
            </div>
            <div class="metrics-pill">
                <span class="metrics-pill-label">Collaboration</span>
                <span class="metrics-pill-value">Groups & Shared Trips</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==================================
# FLIGHTS PAGE
# ==================================
elif page == "Flights":
    require_login()

    st.markdown("### ✈️ Flight Intelligence Hub")

    with st.container():
        col_l, col_r = st.columns([1.4, 1])

        # ---- Flight Price Prediction ----
        with col_l:
            st.markdown("#### 💰 Flight Price Prediction")
            st.caption("Estimate your fare instantly using our ML model.")

            col1, col2, col3 = st.columns(3)
            with col1:
                stops = st.number_input(
                    "Number of stops", min_value=0, max_value=3, value=0
                )
                duration_mins = st.number_input(
                    "Duration (mins)", min_value=30, value=120
                )
            with col2:
                days_to_dep = st.number_input("Days to departure", min_value=0, value=30)
                departure_date = st.date_input("Departure Date", value=date.today())
            with col3:
                airline = st.selectbox(
                    "Airline", ["Indigo", "Air India", "SpiceJet", "Vistara"]
                )
                source = st.selectbox("Source", ["DEL", "HYD", "GOI", "BOM"])
                destination = st.selectbox(
                    "Destination", ["DEL", "GOI", "HYD", "BOM"]
                )

            if st.button("Predict Price", key="price_predict"):
                def norm_key(s: str) -> str:
                    return s.replace(" ", "").replace("-", "").replace(".", "")

                onehot_payload = {
                    "stops": int(stops),
                    "duration_mins": int(duration_mins),
                    "days_to_dep": int(days_to_dep),
                    f"airline_{norm_key(airline)}": 1,
                    f"source_{norm_key(source)}": 1,
                    f"destination_{norm_key(destination)}": 1,
                }

                original_payload = {
                    "airline": airline,
                    "source": source,
                    "destination": destination,
                    "departure_date": str(departure_date),
                    "stops": int(stops),
                    "duration_mins": int(duration_mins),
                    "days_to_dep": int(days_to_dep),
                }

                try:
                    resp = requests.post(
                        f"{API_BASE}/price/predict_price",
                        json=onehot_payload,
                        timeout=15,
                    )
                except Exception as e:
                    st.error(f"Network error when calling price API: {e}")
                    resp = None

                if not resp or not resp.ok:
                    try:
                        resp2 = requests.post(
                            f"{API_BASE}/price/predict_price",
                            json=original_payload,
                            timeout=15,
                        )
                    except Exception as e:
                        st.error(
                            f"Network error when calling price API (fallback): {e}"
                        )
                        resp2 = None

                    if resp2 and resp2.ok:
                        try:
                            price = resp2.json().get("predicted_price")
                            st.success(f"Predicted Price: ₹{int(price)}")
                        except Exception:
                            st.error(
                                f"Unexpected response (fallback): {resp2.status_code} {resp2.text}"
                            )
                    else:
                        code = resp2.status_code if resp2 else "no-response"
                        text = resp2.text if resp2 else ""
                        st.error(
                            f"Error fetching prediction (fallback). Status: {code}. {text}"
                        )
                else:
                    try:
                        price = resp.json().get("predicted_price")
                        st.success(f"Predicted Price: ₹{int(price)}")
                    except Exception:
                        st.error(f"Unexpected response: {resp.status_code} {resp.text}")

        # ---- Carbon Footprint ----
        with col_r:
            st.markdown("#### 🌍 Carbon Footprint")
            st.caption("Estimate total and per-passenger CO₂ emissions.")

            distance = st.number_input(
                "Flight Distance (km):", min_value=1, key="carbon_distance"
            )
            passengers = st.number_input(
                "Number of Passengers:", min_value=1, step=1, key="carbon_passengers"
            )

            if st.button("Calculate Carbon", key="carbon_calc"):
                payload = {"distance_km": distance, "passengers": passengers}

                # Try multiple likely endpoints under /ai prefix (as in main.py)
                endpoints = [
                    "/ai/carbon",
                    "/ai/carbon/estimate",
                    "/ai/carbon_footprint",
                ]
                success = False
                last_resp = None
                last_err = None

                for path in endpoints:
                    try:
                        resp = requests.post(
                            f"{API_BASE}{path}", json=payload, timeout=15
                        )
                        last_resp = resp
                    except Exception as e:
                        last_err = e
                        continue

                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            st.success("Carbon Footprint Result")
                            st.write(f"Distance: {data.get('distance_km')} km")
                            st.write(f"Passengers: {data.get('passengers')}")
                            st.write(f"Total CO₂: {data.get('total_co2_kg')} kg")
                            st.write(
                                f"Per-person CO₂: {data.get('per_person_kg')} kg"
                            )
                            st.caption(f"(Endpoint used: {path})")
                            success = True
                        except Exception:
                            st.error(
                                f"Unexpected response from {path}: "
                                f"{resp.status_code} {resp.text}"
                            )
                        break  # stop trying once we got a 200

                if not success:
                    if last_err is not None and last_resp is None:
                        st.error(f"Carbon API network error: {last_err}")
                    elif last_resp is not None:
                        st.error(
                            f"Carbon API error: {last_resp.status_code} {last_resp.text}"
                        )
                    else:
                        st.error("Carbon API error: No response from any endpoint.")

    st.markdown("---")

    # ---- Disruption Simulator ----
    st.markdown("#### ⚠️ Disruption Simulator")
    st.caption("Stress-test your itinerary against potential delays and disruptions.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        airline_d = st.text_input("Airline", key="disrupt_airline")
    with col2:
        source_d = st.text_input("Source Airport Code", key="disrupt_source")
    with col3:
        destination_d = st.text_input(
            "Destination Airport Code", key="disrupt_destination"
        )
    with col4:
        departure_time_d = st.text_input(
            "Departure Time (YYYY-MM-DDTHH:MM:SS)", key="disrupt_time"
        )

    if st.button("Simulate Disruption", key="disrupt_simulate"):
        payload = {
            "airline": airline_d,
            "source": source_d,
            "destination": destination_d,
            "departure_time": departure_time_d,
        }
        try:
            response = requests.post(
                f"{API_BASE}/disruptions/simulate", json=payload, timeout=15
            )
        except Exception as e:
            st.error(f"Network error when calling disruption API: {e}")
        else:
            if response.status_code == 200:
                try:
                    data = response.json()
                    st.success("Disruption Simulation Result")
                    st.write(f"Airline: {data['airline']}")
                    st.write(f"Route: {data['source']} → {data['destination']}")
                    st.write(f"Status: **{data['status']}**")
                    if data["status"] == "delayed":
                        st.write(f"Delay: {data['delay_mins']} minutes")
                    st.write(f"Reason: {data['reason']}")
                except Exception:
                    st.error(
                        f"Unexpected response: {response.status_code} {response.text}"
                    )
            else:
                st.error(
                    f"Disruption API error: {response.status_code} {response.text}"
                )

# ==================================
# DESTINATIONS PAGE
# ==================================
elif page == "Destinations":
    require_login()

    st.markdown("### 🌍 Destination Studio")

    # ---- Budget Destination Recommender ----
    with st.container():
        st.markdown("#### 💸 Budget Destination Recommender")
        st.caption("Tell us your budget and vibe; we’ll shortlist perfect cities.")

        col_a, col_b = st.columns(2)
        with col_a:
            budget = st.number_input(
                "Enter budget (INR)", min_value=1000, value=20000, key="dest_budget"
            )
            days = st.number_input(
                "Trip days", min_value=1, value=5, key="dest_days"
            )
        with col_b:
            prefs = st.multiselect(
                "Preferences",
                ["beach", "culture", "adventure"],
                default=["culture"],
                key="dest_prefs",
            )

        if st.button("Recommend Destinations", key="dest_recommend"):
            payload = {
                "budget_total": float(budget),
                "trip_days": int(days),
                "preferences": prefs,
            }
            try:
                resp = requests.post(
                    f"{API_BASE}/destination/recommend_destinations",
                    json=payload,
                    timeout=20,
                )
            except Exception as e:
                st.error(f"Network error when calling recommender API: {e}")
                resp = None

            if resp and resp.ok:
                try:
                    results = resp.json()
                    if results:
                        st.table(results)
                    else:
                        st.info(
                            "No destinations found for the given budget/preferences."
                        )
                except Exception:
                    st.error(
                        f"Unexpected response format: {resp.status_code} {resp.text}"
                    )
            elif resp:
                st.error(f"Error calling API: {resp.status_code}. {resp.text}")

    st.markdown("---")

    # ---- Personalized Destination Discovery (AI) ----
    with st.container():
        st.markdown("#### 🤖 Personalized Destination Discovery (AI)")
        st.caption("Describe your dream trip and let the AI craft tailored ideas.")

        col1, col2 = st.columns([1.1, 1])
        with col1:
            ai_name = st.text_input("Your name", "Traveler", key="ai_name")
            ai_prefs = st.text_input(
                "Tell the AI your preferences", "beach and culture", key="ai_prefs"
            )
            ai_budget = st.number_input(
                "Budget (INR)", min_value=500, value=3000, key="ai_budget"
            )

        if "ai_running" not in st.session_state:
            st.session_state.ai_running = False

        with col2:
            if st.button(
                "Get AI Suggestions",
                key="ai_suggest",
                disabled=st.session_state.ai_running,
            ):
                st.session_state.ai_running = True
                payload = {
                    "user_name": ai_name,
                    "preferences": ai_prefs,
                    "budget": float(ai_budget),
                }
                with st.spinner("Getting AI suggestions..."):
                    try:
                        resp = requests.post(
                            f"{API_BASE}/ai/personalized_discovery",
                            json=payload,
                            timeout=30,
                        )
                    except Exception as e:
                        st.error(f"Network error: {e}")
                    else:
                        if resp.ok:
                            try:
                                data = resp.json()
                                recs = data.get("recommendations", [])
                                note = data.get("note")
                                cached_flag = data.get("cached", False)
                                if note:
                                    st.info("Server note: " + str(note))
                                if cached_flag:
                                    st.info("Returned from cache (fast).")
                                if recs:
                                    cols = st.columns(max(1, len(recs)))
                                    for col, r in zip(cols, recs):
                                        with col:
                                            st.markdown(f"**{r.get('rank', '')}.**")
                                            st.write(r.get("text", ""))
                                else:
                                    st.info("No AI recommendations returned.")
                            except Exception:
                                st.error(
                                    f"Unexpected response: {resp.status_code} {resp.text}"
                                )
                        else:
                            st.error(f"AI error: {resp.status_code} {resp.text}")
                st.session_state.ai_running = False

# ==================================
# AI TOOLS PAGE
# ==================================
elif page == "AI Tools":
    require_login()

    st.markdown("### ⚡ Smart Travel Assistant Suite")

    # ---------- Chatbot ----------
    with st.container():
        st.markdown("#### 💬 Skyway Chatbot")
        st.caption("Ask anything about trips, flights, packing or safety.")

        user_message = st.text_input("Your question or message:", key="chat_message")

        if st.button("Send to Chatbot", key="chat_send"):
            if not user_message.strip():
                st.warning("Please enter a message first.")
            else:
                payload = {
                    "message": user_message,
                    "user_id": st.session_state.user_id,
                }
                try:
                    response = requests.post(
                        f"{API_BASE}/assistant/chat", json=payload, timeout=60
                    )
                except Exception as e:
                    st.error(f"Chatbot error: {e}")
                else:
                    if response.ok:
                        try:
                            data = response.json()
                            reply = (
                                data.get("reply")
                                or data.get("answer")
                                or str(data)
                            )
                            st.markdown("**Assistant:** " + reply)
                        except Exception:
                            st.error(
                                f"Unexpected chatbot response: "
                                f"{response.status_code} {response.text}"
                            )
                    else:
                        st.error(
                            f"Chatbot API error: {response.status_code} {response.text}"
                        )

    st.markdown("---")

    # ---------- Travel Itinerary ----------
    with st.container():
        st.markdown("#### 🗺️ Travel Itinerary Generator")
        st.caption("Get a day-by-day plan for your next city.")

        col1, col2 = st.columns([1.2, 1])
        with col1:
            destination = st.text_input("Destination city:", key="iti_city")
        with col2:
            days = st.number_input(
                "Number of days:", min_value=1, step=1, key="iti_days"
            )

        if st.button("Generate Itinerary", key="iti_generate"):
            payload = {"city": destination, "trip_days": int(days)}
            try:
                response = requests.post(
                    f"{API_BASE}/ai/itinerary", json=payload, timeout=30
                )
            except Exception as e:
                st.error(f"Itinerary error: {e}")
            else:
                if response.ok:
                    st.json(response.json())
                else:
                    st.error(
                        f"Itinerary API error: {response.status_code} {response.text}"
                    )

    st.markdown("---")

    # ---------- Packing Suggestions ----------
    with st.container():
        st.markdown("#### 🎒 Packing Suggestions")
        st.caption("Smart packing list based on trip type, weather and duration.")

        trip_type = st.selectbox(
            "Trip Type:", ["Business", "Vacation", "Adventure"], key="pack_type"
        )
        pack_city = st.text_input("City:", "delhi", key="pack_city")
        pack_days = st.number_input(
            "Trip days:", min_value=1, step=1, key="pack_days"
        )
        pack_month = st.selectbox(
            "Month of travel:",
            [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec",
            ],
            key="pack_month",
        )

        if st.button("Get Packing List", key="pack_get"):
            month_to_int = {
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "may": 5,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12,
            }
            payload = {
                "trip_type": trip_type,
                "city": pack_city,
                "trip_days": int(pack_days),
                "month": month_to_int[pack_month],
            }
            try:
                response = requests.post(
                    f"{API_BASE}/planner/packing", json=payload, timeout=30
                )
            except Exception as e:
                st.error(f"Packing error: {e}")
            else:
                if response.ok:
                    st.json(response.json())
                else:
                    st.error(
                        f"Packing API error: {response.status_code} {response.text}"
                    )

    st.markdown("---")

    # ---------- Health Tips ----------
    with st.container():
        st.markdown("#### 🩺 Travel Health & Safety Alerts")
        st.caption("City-specific health advice based on month and country.")

        col1, col2, col3 = st.columns(3)
        with col1:
            health_city = st.text_input("City:", "delhi", key="health_city")
        with col2:
            health_country = st.text_input("Country:", "India", key="health_country")
        with col3:
            health_month = st.selectbox(
                "Month:",
                [
                    "jan",
                    "feb",
                    "mar",
                    "apr",
                    "may",
                    "jun",
                    "jul",
                    "aug",
                    "sep",
                    "oct",
                    "nov",
                    "dec",
                ],
                key="health_month",
            )

        if st.button("Get Health Advice", key="health_get"):
            month_to_int = {
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "may": 5,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12,
            }
            payload = {
                "city": health_city,
                "country": health_country,
                "month": month_to_int[health_month],
            }
            try:
                response = requests.post(
                    f"{API_BASE}/alerts/health", json=payload, timeout=30
                )
            except Exception as e:
                st.error(f"Health error: {e}")
            else:
                if response.ok:
                    st.json(response.json())
                else:
                    st.error(
                        f"Health API error: {response.status_code} {response.text}"
                    )

    st.markdown("---")

    # ---------- Savings Calculator ----------
    with st.container():
        st.markdown("#### 💼 Savings & Salary Planner")
        st.caption("Distribute your budget into smart daily limits for the trip.")

        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input(
                "Total trip budget (₹):", min_value=0.0, key="sav_budget"
            )
        with col2:
            duration = st.number_input(
                "Trip duration (days):", min_value=1.0, key="sav_duration"
            )

        if st.button("Calculate Savings", key="sav_calc"):
            payload = {
                "budget": float(budget),
                "duration_days": int(duration),
            }
            try:
                response = requests.post(
                    f"{API_BASE}/ai/savings", json=payload, timeout=20
                )
            except Exception as e:
                st.error(f"Savings API network error: {e}")
            else:
                if response.ok:
                    try:
                        data = response.json()
                        st.success("Savings Plan")
                        st.write(f"Total Budget: ₹{data.get('total_budget')}")
                        st.write(f"Trip Days: {data.get('duration_days')}")
                        st.write(
                            f"Daily Spend Limit: ₹{data.get('daily_budget')}"
                        )
                        if data.get("message"):
                            st.info(data["message"])
                    except Exception:
                        st.error(
                            f"Unexpected savings response: "
                            f"{response.status_code} {response.text}"
                        )
                else:
                    st.error(
                        f"Savings API error: {response.status_code} {response.text}"
                    )

# ==================================
# PROFILE PAGE
# ==================================
elif page == "Profile":
    require_login()

    st.markdown("### 👤 Traveler Profile")

    profile_data = None
    try:
        resp = requests.get(
            f"{API_BASE}/profile/{st.session_state.user_id}", timeout=10
        )
    except Exception as e:
        st.error(f"Error fetching profile: {e}")
        resp = None

    if resp and resp.status_code == 200:
        try:
            profile_data = resp.json()
            st.success("Profile Info")
            st.table([profile_data])
        except Exception:
            st.error(f"Unexpected profile response: {resp.status_code} {resp.text}")
    elif resp:
        try:
            detail = resp.json().get("detail", "Profile not found")
        except Exception:
            detail = f"Profile not found. Status {resp.status_code}: {resp.text}"
        st.error(detail)

    existing_name = (
        profile_data.get("name") if profile_data else st.session_state.user_name
    )
    existing_email = profile_data.get("email") if profile_data else ""
    existing_home = profile_data.get("home_airport") if profile_data else "HYD"
    existing_salary = (
        float(profile_data.get("monthly_salary", 0)) if profile_data else 0.0
    )
    existing_savings = (
        float(profile_data.get("monthly_savings", 0)) if profile_data else 0.0
    )
    existing_themes = profile_data.get("themes", "culture") if profile_data else "culture"
    existing_budget = float(profile_data.get("usual_budget", 0)) if profile_data else 0.0
    existing_trip_len = (
        int(profile_data.get("trip_length_days", 1)) if profile_data else 1
    )

    st.markdown("#### Update / Create Profile")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input(
            "Name:", value=existing_name, key="prof_name"
        )
        email = st.text_input(
            "Email:", value=existing_email, key="prof_email"
        )
        home_airport = st.text_input(
            "Home Airport:", value=existing_home, key="prof_home"
        )
    with col2:
        monthly_salary = st.number_input(
            "Monthly Salary:",
            min_value=0.0,
            step=1000.0,
            value=existing_salary,
            key="prof_salary",
        )
        monthly_savings = st.number_input(
            "Monthly Savings:",
            min_value=0.0,
            step=500.0,
            value=existing_savings,
            key="prof_savings",
        )

    themes = st.text_input(
        "Favourite travel themes (comma-separated):",
        value=str(existing_themes),
        key="prof_themes",
    )
    usual_budget = st.number_input(
        "Usual trip budget (₹):",
        min_value=0.0,
        step=5000.0,
        value=existing_budget,
        key="prof_budget",
    )
    trip_length_days = st.number_input(
        "Usual trip length (days):",
        min_value=1,
        step=1,
        value=existing_trip_len,
        key="prof_trip_len",
    )

    if st.button("Save Profile", key="prof_save"):
        payload = {
            "user_id": st.session_state.user_id,
            "name": username,
            "email": email,
            "home_airport": home_airport,
            "monthly_salary": monthly_salary,
            "monthly_savings": monthly_savings,
            "themes": themes,
            "usual_budget": usual_budget,
            "trip_length_days": int(trip_length_days),
        }
        try:
            resp = requests.post(
                f"{API_BASE}/profile/create", json=payload, timeout=10
            )
        except Exception as e:
            st.error(f"Error saving profile: {e}")
        else:
            if resp.status_code == 200:
                st.success("Profile updated/created successfully!")
                try:
                    refreshed = requests.get(
                        f"{API_BASE}/profile/{st.session_state.user_id}", timeout=10
                    )
                    if refreshed.ok:
                        st.info("Latest profile from server:")
                        st.table([refreshed.json()])
                except Exception as e:
                    st.warning(f"Profile saved but re-fetch failed: {e}")
            else:
                try:
                    detail = resp.json().get("detail", "Profile update failed")
                except Exception:
                    detail = (
                        f"Profile update failed. Status {resp.status_code}: {resp.text}"
                    )
                st.error(detail)

# ==================================
# GROUP TRAVEL PAGE
# ==================================
elif page == "Group Travel":
    require_login()

    st.markdown("### 👥 Group Travel Planner")

    st.markdown("#### Create Group")
    col1, col2 = st.columns(2)
    with col1:
        group_name = st.text_input("Group Name", key="grp_name")
        trip_city = st.text_input("Trip City", key="grp_city")
    with col2:
        trip_start_date = st.date_input("Trip Start Date", key="grp_start")
        trip_end_date = st.date_input("Trip End Date", key="grp_end")

    if st.button("Create Group", key="grp_create"):
        payload = {
            "name": group_name,
            "trip_city": trip_city,
            "trip_start_date": str(trip_start_date),
            "trip_end_date": str(trip_end_date),
            "owner_user_id": st.session_state.user_id,
        }
        try:
            resp = requests.post(
                f"{API_BASE}/groups/create", json=payload, timeout=10
            )
        except Exception as e:
            st.error(f"Error creating group: {e}")
        else:
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    st.success(f"Group created! Group ID: {data['group_id']}")
                except Exception:
                    st.error(f"Unexpected response: {resp.status_code} {resp.text}")
            else:
                try:
                    detail = resp.json().get("detail", "Group creation failed")
                except Exception:
                    detail = (
                        f"Group creation failed. Status {resp.status_code}: {resp.text}"
                    )
                st.error(detail)

    st.markdown("---")

    st.markdown("#### View Group")
    col1, _ = st.columns([1, 3])
    with col1:
        view_group_id = st.number_input(
            "Enter Group ID to View", min_value=1, step=1, key="grp_view_id"
        )

    if st.button("Get Group Info", key="grp_get"):
        try:
            resp = requests.get(
                f"{API_BASE}/groups/{view_group_id}", timeout=10
            )
        except Exception as e:
            st.error(f"Error fetching group: {e}")
        else:
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    st.success("Group Info")
                    st.table([data["group"]])
                    st.write("Members:")
                    st.table(data["members"])
                except Exception:
                    st.error(f"Unexpected response: {resp.status_code} {resp.text}")
            else:
                try:
                    detail = resp.json().get("detail", "Group not found")
                except Exception:
                    detail = (
                        f"Group not found. Status {resp.status_code}: {resp.text}"
                    )
                st.error(detail)
