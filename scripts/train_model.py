import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

#paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SILVER_DATA_PATH = os.path.join(BASE_DIR, "data", "silver_taxi_data")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "models", "taxi_duration_model.pkl")
# making sure of the path existence
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# read data and minimise it for training
df = pd.read_parquet(SILVER_DATA_PATH).head(50000)

features = ["pickuphour", "dayof_week", "month", "congestion_surcharge",
            "trip_distance", "PULocationID", "DOLocationID",
            "cbd_congestion_fee", "total_amount"]
X = df[features]
y = df["duration_minutes"]

# training
rf = RandomForestRegressor(n_estimators=20, max_depth=8, n_jobs=1, random_state=42)
rf.fit(X, y)
# saving the model
joblib.dump(rf, MODEL_SAVE_PATH)
print(f"Model saved successfully to {MODEL_SAVE_PATH}")