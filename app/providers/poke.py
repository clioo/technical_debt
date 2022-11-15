import requests
from typing import List, Dict, Optional, Union
from urllib.parse import urlencode


BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemons(offset: int = 0, limit: int = 20) -> List[Dict]:
    query_params = {"offset": offset, "limit": limit}
    query_str = urlencode(query_params)

    url = f"{BASE_URL}/pokemon?{query_str}"
    res = requests.get(url=url)

    if res.status_code == 200:
        return res.json().get("results")
    raise Exception("[1234] Wrong api call to Pokemon API.")


def get_pokemon(identifier: Union[int, str]) -> Optional[Dict]:
    url = f"{BASE_URL}/pokemon/{identifier}"
    res = requests.get(url=url)
    if res.status_code == 200:
        return res.json()
