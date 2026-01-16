from pydantic import BaseModel
#schema pydantic 
class TripInput(BaseModel):
    pickuphour: int
    dayof_week: int
    month: int
    trip_distance: float
    PULocationID: int
    DOLocationID: int
    congestion_surcharge: float
    cbd_congestion_fee: float
    total_amount: float
class UserCreate(BaseModel):
    username: str
    password: str