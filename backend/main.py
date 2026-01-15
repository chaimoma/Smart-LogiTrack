from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import joblib
import pandas as pd
from .database import engine, get_db, Base
from .models import ETAPrediction
from .schemas import TripInput
from .auth import verify_token, create_token
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Smart LogiTrack ETA API")

# load model
model = joblib.load("models/taxi_duration_model.pkl")
MODEL_VERSION = "v1"

# token endpoint
@app.get("/token")
def get_token():
    token = create_token()
    return {"token": token}

# endpoints 
@app.post("/predict")
def predict(trip: TripInput, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    df = pd.DataFrame([trip.model_dump()])
    features = ["pickuphour","dayof_week","month","congestion_surcharge",
                "trip_distance","PULocationID","DOLocationID",
                "cbd_congestion_fee","total_amount"]
    X = df[features]
    prediction = model.predict(X)
    pred_duration = float(prediction[0])

    #saving to db
    db.add(ETAPrediction(
        **trip.model_dump(),
        predicted_duration=pred_duration,
        model_version=MODEL_VERSION,
        created_at=datetime.utcnow()
    ))
    db.commit()

    return {"estimated_duration": pred_duration}

# analytics
# avg wqt dkola sa3a
@app.get("/analytics/avg-duration-by-hour")
def avg_duration_by_hour(db: Session = Depends(get_db),token:str=Depends(verify_token)):
    sql = """
    WITH duration_calc AS (
        SELECT 
            EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickuphour,
            EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime))/60 AS duration_minutes
        FROM taxi_silver
        WHERE EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) > 0
    )
    SELECT pickuphour, AVG(duration_minutes) AS avgduration
    FROM duration_calc
    GROUP BY pickuphour
    ORDER BY pickuphour
    """
    result = db.execute(text(sql))
    return [{"pickuphour": int(row[0]), "avgduration": float(row[1])} for row in result]

# avg duration lkola payement type 
@app.get("/analytics/payment-analysis")
def payment_analysis(db: Session = Depends(get_db),token: str=Depends(verify_token)):
    sql = """
    WITH duration_calc AS (
        SELECT 
            payment_type,
            EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime))/60 AS duration_minutes
        FROM taxi_silver
        WHERE EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) > 0
    )
    SELECT payment_type, COUNT(*) AS total_trips, AVG(duration_minutes) AS avg_duration
    FROM duration_calc
    GROUP BY payment_type
    ORDER BY payment_type
    """
    result = db.execute(text(sql))
    return [{"payment_type": int(row[0]), "total_trips": int(row[1]), "avg_duration": float(row[2])} for row in result]
