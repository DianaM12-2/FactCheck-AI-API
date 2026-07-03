import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"


def test_get_all_claims(client):
    res = client.get("/api/v1/claims")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_create_claim_valid(client):
    res = client.post("/api/v1/claims", json={
        "patient_name": "Test Patient",
        "medication": "TestDrug",
        "amount": 75.00
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["patient"] == "Test Patient"
    assert data["amount"] == 75.00
    assert "claim_id" in data


def test_create_claim_missing_fields(client):
    res = client.post("/api/v1/claims", json={"patient_name": "Test"})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_high_value_claim_flagged(client):
    res = client.post("/api/v1/claims", json={
        "patient_name": "High Value Patient",
        "medication": "Specialty Drug",
        "amount": 750.00
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["flagged"] is True
    assert data["status"] == "flagged"


def test_get_claim_not_found(client):
    res = client.get("/api/v1/claims/RX-INVALID-999")
    assert res.status_code == 404


def test_get_flagged_claims(client):
    res = client.get("/api/v1/claims/flagged")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_analytics_endpoint(client):
    res = client.get("/api/v1/claims/analytics")
    assert res.status_code == 200
    data = res.get_json()
    assert "total_claims" in data
    assert "total_amount" in data
    assert "flagged_count" in data


def test_factcheck_missing_claim(client):
    res = client.post("/api/v1/factcheck", json={})
    assert res.status_code == 400


def test_factcheck_demo_mode(client):
    res = client.post("/api/v1/factcheck", json={"claim": "The Earth is flat."})
    assert res.status_code in [200, 207]
    data = res.get_json()
    assert "verdict" in data
    assert "confidence" in data
    assert "explanation" in data


def test_delete_claim(client):
    create_res = client.post("/api/v1/claims", json={
        "patient_name": "Delete Me",
        "medication": "Drug",
        "amount": 50.00
    })
    claim_id = create_res.get_json()["claim_id"]
    del_res = client.delete(f"/api/v1/claims/{claim_id}")
    assert del_res.status_code == 204
