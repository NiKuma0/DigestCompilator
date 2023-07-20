from fastapi.testclient import TestClient


def test_healhcheck(testclient: TestClient):
    response = testclient.get("/api/healthcheck")
    assert response.status_code == 200
    assert response.json() == "OK"
