from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestHealthcheck:

    def test_healthcheck_success(self):
        response = client.get("/healthcheck")
        assert response.status_code == 200
        assert response.json() == {"message": "OK!"}
