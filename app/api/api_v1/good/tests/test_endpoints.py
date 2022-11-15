from main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

BASE_PATH = "/api/v1/good"


class TestHealthcheck:
    def test_healthcheck_success(self):
        response = client.get("/api/v1/good/healthcheck")
        assert response.status_code == 200
        assert response.json() == {"message": "OK!"}

    def test_get_pokemon(self, mocker):
        with open("api/api_v1/good/tests/test_data/charizard.json") as file:
            charizard_json_res = json.load(file)
        get_pokemon_mock = mocker.patch(
            "api.api_v1.good.good_service.poke_provider.get_pokemon",
            return_value=charizard_json_res,
        )
        res = client.get(f"{BASE_PATH}/pokemon/charizard")
        get_pokemon_mock.assert_called_once()
        assert res.status_code == 200
        assert res.json() == charizard_json_res
