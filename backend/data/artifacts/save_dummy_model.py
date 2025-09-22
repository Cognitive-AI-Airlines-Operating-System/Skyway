# save_dummy_model.py
import joblib

class DummyModel:
    def predict(self, X):
        return [9999] * len(X)  # Always returns 9999 as price

dummy = DummyModel()
joblib.dump(dummy, "data/artifacts/price_model.joblib")
print("✅ Dummy model saved at data/artifacts/price_model.joblib")
