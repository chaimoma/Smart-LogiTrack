from fastapi.testclient import TestClient
import sys
import os

# add the project root directory to sys.path so Python can find the 'backend' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app 

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "pickuphour": 10,
        "dayof_week": 1,
        "month": 1,
        "trip_distance": 5.5,
        "PULocationID": 100,
        "DOLocationID": 200,
        "congestion_surcharge": 2.5,
        "cbd_congestion_fee": 0.0,
        "total_amount": 25.0
    }
    response = client.post(
        "/predict", 
        json=payload,
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code in [200, 401]