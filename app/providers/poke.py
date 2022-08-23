import requests
from urllib.parse import urlencode


BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemons(offset: int = 20, limit: int = 20) -> dict:
    query_params = {
        "offset": offset,
        "limit": limit
    }
    query_str = urlencode(query_params)

    url = f"{BASE_URL}/pokemon?{query_str}"
    res = requests.get(url=url)
    return res.json().get("results")

