from typing import Union
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from providers import poke as poke_provider
from business_logic import logic as business_logic
from urllib.parse import urlencode
import requests


bad_router = APIRouter(prefix="/api/v1/bad")


@bad_router.get("/healthcheck")
def get_service1_healthcheck():
    # Do your healthcheck for your specific service here
    return JSONResponse(content={"message": "OK!"}, status_code=status.HTTP_200_OK)


@bad_router.get("/pokemons")
def get_pokemons(limit: int = 20, offset: int = 20):
    query_params = {"offset": offset, "limit": limit}
    query_str = urlencode(query_params)

    url = f"https://pokeapi.co/api/v2/pokemon?{query_str}"
    res = requests.get(url=url)

    if res.status_code == 200:
        return res.json().get("results")
    raise Exception("[1234] Wrong api call to Pokemon API.")


@bad_router.get("/pokemon/{identifier}")
def get_pokemon(identifier: Union[int, str]):
    url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    res = requests.get(url=url)
    if res.status_code == 200:
        return res.json()
    return JSONResponse(
        content={"error_code": 1001, "detail": "Pokemon not found"}, status_code=404
    )


@bad_router.get("/get_stronger_pokemon_than/{identifier}")
def get_stronger_pokemon_than(identifier: Union[int, str]):

    my_pokemon_data = poke_provider.get_pokemon(identifier=identifier)
    my_pokemon_attack = None
    for stat in my_pokemon_data.get("stats", []):
        if stat.get("stat").get("name") == "attack":
            my_pokemon_attack = stat.get("base_stat")
    if not my_pokemon_attack:
        raise Exception("[1002] No stat name found in that pokemon.")
    offset = 0
    pokemons = poke_provider.get_pokemons(offset=offset)
    while pokemons:
        for pokemon_data in pokemons:
            pokemon_full_stats = poke_provider.get_pokemon(
                identifier=pokemon_data.get("name")
            )
            challenger_value = None
            for stat in pokemon_full_stats.get("stats", []):
                if stat.get("stat").get("name") == "attack":
                    challenger_value = stat.get("base_stat")
            if not challenger_value:
                raise Exception("[1002] No stat name found in that pokemon.")
            if challenger_value > my_pokemon_attack:
                stronger_pokemon = pokemon_data
        # Next pokemon page
        offset += 20
        pokemons = poke_provider.get_pokemons(offset=offset)

    stronger_pokemon = business_logic.get_stronger_pokemon_than(identifier=identifier)
    if stronger_pokemon:
        return stronger_pokemon
    return JSONResponse(
        content={
            "error_code": 1005,
            "detail": "There is no stronger pokemon than this!",
        },
        status_code=404,
    )
