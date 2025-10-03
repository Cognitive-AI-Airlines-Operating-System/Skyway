# backend/app/models/train_price_model.py
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# 1) Paths
ROOT = Path(__file__).resolve().parents[2]  # backend/
RAW = ROOT / "data" / "raw" / "flights_sample.csv"
ART = ROOT / "data" / "artifacts"
ART.mkdir(parents=True, exist_ok=True)

# 2) Load data
df = pd.read_csv(RAW, parse_dates=["departure_date"])

# 3) Feature engineering
df["month"] = df["departure_date"].dt.month
df["dow"]   = df["departure_date"].dt.dayofweek

features = ["airline", "source", "destination", "stops", "duration_mins", "days_to_dep", "month", "dow"]
target = "base_price"

X = df[features].copy()
y = df[target].copy()

# 4) Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5) Preprocessing pipeline
cat_cols = ["airline", "source", "destination"]
num_cols = ["stops", "duration_mins", "days_to_dep", "month", "dow"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", StandardScaler(), num_cols)
    ],
    remainder="drop",
)

# 6) Model
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)

pipe = Pipeline([("pre", preprocessor), ("model", model)])

# 7) Train
pipe.fit(X_train, y_train)

# 8) Evaluate
preds = pipe.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print(f"MAE: {mae:.2f}")

# 9) Save model & metrics
joblib.dump(pipe, ART / "price_model.joblib")
with open(ART / "price_model_metrics.txt", "w") as f:
    f.write(f"MAE={mae:.2f}\n")

print("✅ Model trained and saved at:", ART / "price_model.joblib")
