# backend/app/models/train_recommender.py
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import joblib

ROOT = Path(__file__).resolve().parents[2]  # backend/
RAW = ROOT / "data" / "raw" / "destinations.csv"
PROC = ROOT / "data" / "processed"
ART  = ROOT / "data" / "artifacts"
PROC.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)

# 1) Ensure numeric
df["avg_daily_cost"] = pd.to_numeric(df["avg_daily_cost"], errors="coerce").fillna(df["avg_daily_cost"].median())

# 2) Theme columns exist as int
theme_cols = ["theme_beach", "theme_culture", "theme_adventure"]
for c in theme_cols:
    if c not in df.columns:
        df[c] = 0
    df[c] = df[c].astype(int)

# 3) Normalize avg_daily_cost for scoring later
scaler = MinMaxScaler()
df["cost_norm"] = scaler.fit_transform(df[["avg_daily_cost"]])

# 4) Save processed CSV and scaler
df.to_csv(PROC / "destinations_processed.csv", index=False)
joblib.dump(scaler, ART / "dest_scaler.joblib")
joblib.dump(theme_cols, ART / "reco_theme_cols.joblib")
print("Saved processed destinations and artifacts.")
