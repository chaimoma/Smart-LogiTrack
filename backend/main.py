from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import joblib
import pandas as pd
from .database import engine, get_db, Base
from .models import ETAPrediction,User
from .schemas import TripInput, UserCreate
from .auth import verify_token, create_token,verify_password,hash_password
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Smart LogiTrack ETA API")

# load model
model = joblib.load("models/taxi_duration_model.pkl")
MODEL_VERSION = "v1"

# endpoints 
# register user
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

# login user
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token()
    return {"access_token": token, "token_type": "bearer"}

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
