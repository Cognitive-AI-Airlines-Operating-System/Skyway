import requests
r = requests.post("http://localhost:8000/api/predict_price", json={
    "airline":"Indigo","source":"HYD","destination":"DEL","departure_date":"2025-10-15","stops":0,"duration_mins":120,"days_to_dep":40})
print(r.status_code, r.json())

