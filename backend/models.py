from sqlalchemy import Column, Integer, Float, DateTime, String,BigInteger
from .database import Base
#table for saving predictions
class ETAPrediction(Base):
    __tablename__ = "eta_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pickuphour = Column(Integer)
    dayof_week = Column(Integer)
    month = Column(Integer)
    trip_distance = Column(Float)
    PULocationID = Column(Integer)
    DOLocationID = Column(Integer)
    congestion_surcharge = Column(Float)
    cbd_congestion_fee = Column(Float)
    total_amount = Column(Float)
    predicted_duration = Column(Float)
    model_version = Column(String(20))
    created_at = Column(DateTime)
#table for silver taxi data (from pipeline ml)
class ETATrip(Base):
    __tablename__ = "taxi_silver"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    VendorID = Column(Integer)
    tpep_pickup_datetime = Column(DateTime)
    tpep_dropoff_datetime = Column(DateTime)
    passenger_count = Column(BigInteger)
    trip_distance = Column(Float)
    RatecodeID = Column(BigInteger)
    store_and_fwd_flag = Column(String)
    PULocationID = Column(Integer)
    DOLocationID = Column(Integer)
    payment_type = Column(BigInteger)
    fare_amount = Column(Float)
    extra = Column(Float)
    mta_tax = Column(Float)
    tip_amount = Column(Float)
    tolls_amount = Column(Float)
    improvement_surcharge = Column(Float)
    total_amount = Column(Float)
    congestion_surcharge = Column(Float)
    Airport_fee = Column(Float)
    cbd_congestion_fee = Column(Float)
