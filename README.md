# ✈️ Skyway

## Cognitive AI Airlines Operating System

Skyway is a Cognitive AI Airlines Operating System designed to provide an intelligent, personalized, and efficient travel experience through AI-powered automation, prediction, recommendation, and optimization.

The platform combines airline operations with Artificial Intelligence to help travelers make smarter decisions before and during their journey.

---

## 🚀 Overview

Skyway brings multiple intelligent travel services together in a unified system.

The system provides:

- ✈️ Flight Price Prediction
- 🌍 Budget-Based Destination Recommendation
- 🤖 Personalized AI Destination Discovery
- 💬 AI Travel Assistant / Chatbot
- 🗺️ AI Travel Itinerary Generation
- 🧳 Smart Packing Suggestions
- ❤️ Travel Health Alerts
- 🌱 Carbon Footprint Estimation
- ⚠️ Flight Disruption Simulation
- 💰 Travel Savings Planning
- 🛣️ Route Optimization
- 👥 Group Travel Management
- 👤 User Profile Management
- 💳 Payment Integration Support

---

## 🧠 Core AI Capabilities

### ✈️ Flight Price Prediction

Predicts estimated flight prices using machine-learning models based on flight-related parameters such as:

- Airline
- Source
- Destination
- Number of Stops
- Flight Duration
- Days Until Departure

---

### 🌍 Budget Destination Recommendation

Recommends destinations based on:

- Total travel budget
- Trip duration
- Travel preferences
- Destination characteristics

Users can select preferences such as:

- Beach
- Culture
- Adventure

---

### 🤖 Personalized AI Destination Discovery

Uses a transformer-based language model to generate personalized destination suggestions based on the traveler's preferences and budget.

The current implementation uses:

`google/flan-t5-small`

---

### 💬 AI Travel Assistant

Provides an AI-powered conversational interface for travel-related assistance.

---

### 🗺️ Intelligent Itinerary Generation

Generates structured travel itineraries based on:

- Destination
- Number of days
- Traveler requirements

---

### 🧳 Smart Packing Planner

Provides packing recommendations based on the type of trip.

---

### ❤️ Travel Health Alerts

Provides travel-related health information based on the selected destination.

---

### 🌱 Carbon Footprint Estimation

Estimates carbon emissions based on:

- Flight distance
- Number of passengers

---

### ⚠️ Disruption Management

Simulates potential flight disruptions and provides information such as:

- Flight status
- Delay duration
- Possible disruption reason

---

### 💰 Savings Planner

Helps travelers estimate and plan their travel savings based on budget and trip duration.

---

### 🛣️ Route Optimization

Uses graph-based optimization techniques to support intelligent travel route planning.

---

### 👥 Group Travel

Provides functionality for creating and managing travel groups, including:

- Group creation
- Trip details
- Group members
- Group information

---

## 🏗️ System Architecture

Skyway follows a modular architecture consisting of a Streamlit frontend and FastAPI backend.

```text
                         ┌─────────────────────────┐
                         │       Skyway UI         │
                         │      Streamlit          │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │        Backend          │
                         └────────────┬────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
      Machine Learning          AI / NLP Models          Travel Services
       & Prediction             Transformers             & Optimization
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │    SQLite     │
                              │    Database   │
                              └───────────────┘

📁 Project Structure

Skyway/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── carbon.py
│   │   │   ├── chatbot.py
│   │   │   ├── disruptions.py
│   │   │   ├── group_travel.py
│   │   │   ├── health_alerts.py
│   │   │   ├── itinerary.py
│   │   │   ├── optimized_route.py
│   │   │   ├── packing.py
│   │   │   ├── payments.py
│   │   │   ├── personalized_discovery.py
│   │   │   ├── price.py
│   │   │   ├── profile.py
│   │   │   ├── reco.py
│   │   │   └── savings.py
│   │   │
│   │   ├── models/
│   │   ├── create_tables.py
│   │   ├── db.py
│   │   └── main.py
│   │
│   └── notebooks/
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md

🛠️ Technology Stack
Frontend
Python
Streamlit
Backend
Python
FastAPI
Uvicorn
Artificial Intelligence & Machine Learning
PyTorch
Transformers
Hugging Face
Scikit-learn
XGBoost
NumPy
Pandas
NetworkX
Database
SQLite
Development
Git
GitHub
Virtual Environments


⚙️ Installation
1. Clone the repository
git clone https://github.com/Cognitive-AI-Airlines-Operating-System/Skyway.git
cd Skyway
2. Create a virtual environment
python3 -m venv venv
3. Activate the virtual environment

macOS / Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt

If additional packages are required by your local environment:

pip install networkx transformers torch
▶️ Running the Application

Skyway consists of two services:

1. Start the FastAPI backend

From the project root:

python -m uvicorn backend.app.main:app --reload --port 8000

The backend will be available at:

http://127.0.0.1:8000
2. Start the Streamlit frontend

Open another terminal:

cd /Users/your-username/Skyway
source venv/bin/activate
streamlit run frontend/app.py

The frontend will normally be available at:

http://localhost:8501
📚 API Documentation

Once the FastAPI backend is running, interactive API documentation is available at:

http://localhost:8000/docs

The API documentation can be used to test the available backend endpoints.

🔐 Authentication

Skyway includes user authentication functionality for:

User registration
User login
User profile management

Authentication-related functionality is implemented through the FastAPI backend and integrated with the Streamlit frontend.


🧪 Testing

Before submitting changes, verify that:

The FastAPI backend starts successfully.
The Streamlit frontend starts successfully.
API endpoints respond correctly.
Authentication works correctly.
Existing AI and travel features continue to work.
No unnecessary files such as virtual environments or local databases are committed.
🔒 Local Files

Local Python virtual environments and SQLite database files should not be committed to the repository.

The project's .gitignore excludes common local development files.

🎯 Project Vision

Skyway aims to evolve into a comprehensive Cognitive AI Airlines Operating System capable of combining:

Prediction + Personalization + Automation + Optimization + Intelligent Assistance

into a unified travel platform.

The long-term objective is to make airline and travel operations more intelligent, adaptive, personalized, and efficient through Artificial Intelligence.

📌 Project Status

Active Development

Skyway is currently under active development, with new AI-powered travel services and system improvements being integrated incrementally.

```
