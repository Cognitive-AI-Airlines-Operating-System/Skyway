# Skyway ✈️
AI-powered airline operating system (mini project) - Week 1 demo.


**Sample Request:**
```json
POST /api/predict_price
{
  "airline": "Indigo",
  "source": "HYD",
  "destination": "DEL",
  "departure_date": "2025-10-15",
  "stops": 0,
  "duration_mins": 120,
  "days_to_dep": 40
}


python backend/tests/test_price.py  (run in powershell)
output :-
200 {'predicted_price': 4330.0}