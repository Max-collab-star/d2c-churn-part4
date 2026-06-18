from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_successful_low_risk_prediction():
    payload = {
        "recency": 5,
        "frequency": 25,
        "monetary": 1250.0,
        "complaints_count": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert "churn_probability" in data
    assert data["risk_status"] == "LOW_RISK"

def test_successful_high_risk_prediction():
    payload = {
        "recency": 95,
        "frequency": 1,
        "monetary": 15.0,
        "complaints_count": 6
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] == 1
    assert data["risk_status"] == "CRITICAL_RISK"

def test_request_validation_boundary_error():
    payload = {
        "recency": -10,
        "frequency": -5,
        "monetary": 100.0,
        "complaints_count": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422