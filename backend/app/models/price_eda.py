# backend/app/models/price_eda.py
import pandas as pd

# 1. Load CSV
df = pd.read_csv("backend/data/raw/flights_sample.csv", parse_dates=["departure_date"])

# 2. Show first 5 rows
print("📌 Sample Rows:")
print(df.head())

# 3. Summary stats for each column
print("\n📊 Summary Statistics:")
print(df.describe(include='all'))

# 4. Check for missing values
print("\n❗ Nulls per column:")
print(df.isna().sum())
