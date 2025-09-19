import pandas as pd

# Load destinations data
d = pd.read_csv("backend/data/raw/destinations.csv")

print("First 5 rows:\n", d.head())  # Preview first rows
print("\nSummary stats:\n", d.describe(include='all'))  # Descriptive stats
print("\nNull values per column:\n", d.isna().sum())  # Missing data check
