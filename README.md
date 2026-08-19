# ✈️ Skyway

## Cognitive AI Airlines Operating System

Skyway is an AI-powered airline operating system designed to provide intelligent, personalized, and efficient travel experiences through artificial intelligence, machine learning, automation, and optimization.

---

## 🚀 Features

- **Flight Price Prediction** — Predict estimated flight prices using machine-learning models.
- **Destination Recommendation** — Recommend destinations based on budget, duration, and travel preferences.
- **Personalized AI Discovery** — Generate personalized destination suggestions using a transformer-based AI model.
- **AI Travel Assistant** — Provide conversational assistance for travel-related queries.
- **AI Itinerary Generator** — Generate travel itineraries based on destination, duration, and requirements.
- **Smart Packing Planner** — Provide packing recommendations for planned trips.
- **Travel Health Alerts** — Provide destination-based travel health information.
- **Carbon Footprint Estimation** — Estimate flight-related carbon emissions.
- **Disruption Management** — Handle simulated flight disruption scenarios.
- **Savings Planner** — Assist users with travel savings planning.
- **Route Optimization** — Support intelligent travel route planning.
- **Group Travel** — Support group creation, trip details, and group members.
- **User Authentication & Profiles** — Support registration, login, and profile management.
- **Payment Integration** — Provide payment integration support.

---

## 🧠 AI Capabilities

### Flight Price Prediction

Predicts estimated flight prices using parameters including:

- Airline
- Source
- Destination
- Number of stops
- Flight duration
- Days until departure

### Personalized Destination Discovery

Skyway uses the transformer model:

```text
google/flan-t5-small
```

to generate personalized destination suggestions based on traveler preferences and budget.

### Destination Recommendation

Recommendations can consider:

- Travel budget
- Trip duration
- Travel preferences
- Destination characteristics

---

## 🏗️ System Architecture

Skyway uses a modular architecture consisting of a **Streamlit frontend**, **FastAPI backend**, AI/ML services, and a SQLite database.

```text
┌─────────────────────────────┐
│        Skyway UI            │
│         Streamlit           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        FastAPI API          │
│          Backend            │
└──────────────┬──────────────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   ┌───────┐ ┌───────┐ ┌──────────────┐
   │  ML   │ │  AI   │ │     Travel   │
   │Models │ │Models │ │ Optimization │
   └───────┘ └───────┘ └──────────────┘
               │
               ▼
       ┌────────────────┐
       │ SQLite Database│
       └────────────────┘
```

---

## 📁 Project Structure

```text
Skyway/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── auth.py
│       │   ├── carbon.py
│       │   ├── chatbot.py
│       │   ├── disruptions.py
│       │   ├── group_travel.py
│       │   ├── health_alerts.py
│       │   ├── itinerary.py
│       │   ├── optimized_route.py
│       │   ├── packing.py
│       │   ├── payments.py
│       │   ├── personalized_discovery.py
│       │   ├── price.py
│       │   ├── profile.py
│       │   ├── reco.py
│       │   └── savings.py
│       │
│       ├── models/
│       ├── create_tables.py
│       ├── db.py
│       └── main.py
│
├── data/
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

| Category            | Technologies                                               |
| ------------------- | ---------------------------------------------------------- |
| **Frontend**        | Python, Streamlit                                          |
| **Backend**         | FastAPI, Uvicorn                                           |
| **AI / ML**         | PyTorch, Transformers, Hugging Face, Scikit-learn, XGBoost |
| **Data Processing** | NumPy, Pandas                                              |
| **Optimization**    | NetworkX                                                   |
| **Database**        | SQLite                                                     |
| **Development**     | Git, GitHub, Python Virtual Environment                    |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Cognitive-AI-Airlines-Operating-System/Skyway.git
cd Skyway
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If required by the local environment:

```bash
pip install networkx transformers torch
```

---

## ▶️ Running the Application

Skyway requires the **FastAPI backend** and **Streamlit frontend** to run.

### Backend

From the project root:

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### Frontend

Open a second terminal and activate the same virtual environment:

```bash
source venv/bin/activate
streamlit run frontend/app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

---

## 📚 API Documentation

Once the FastAPI backend is running, open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI provides interactive documentation and testing for the available API endpoints.

---

## 🔐 Authentication

Skyway supports:

- User registration
- User login
- User profiles
- Session-based frontend authentication

Authentication is implemented through the FastAPI backend and integrated with the Streamlit frontend.

---

## 🧪 Testing

Before submitting changes, verify that:

- The FastAPI backend starts successfully.
- The Streamlit frontend starts successfully.
- API endpoints respond correctly.
- User registration and login work correctly.
- Existing AI and travel features continue to work.
- Local virtual environments are not committed.
- Local database files are not committed.

---

## 📌 Project Status

**Active Development**

Skyway is under active development, with additional AI-powered travel capabilities and system improvements being integrated incrementally.
