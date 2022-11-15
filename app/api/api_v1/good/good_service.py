from typing import Union
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from providers import poke as poke_provider
from business_logic import logic as business_logic


good_router = APIRouter(prefix="/api/v1/good")


@good_router.get("/healthcheck")
def get_service1_healthcheck():
    # Do your healthcheck for your specific service here
    return JSONResponse(content={"message": "OK!"}, status_code=status.HTTP_200_OK)


@good_router.get("/pokemons")
def get_pokemons(limit: int = 20, offset: int = 20):
    return poke_provider.get_pokemons(limit=limit, offset=offset)


@good_router.get("/pokemon/{identifier}")
def get_pokemon(identifier: Union[int, str]):
    pokemon_data = poke_provider.get_pokemon(identifier=identifier)
    if pokemon_data:
        return pokemon_data
    return JSONResponse(
        content={"error_code": 1001, "detail": "Pokemon not found"}, status_code=404
    )


@good_router.get("/get_stronger_pokemon_than/{identifier}")
def get_stronger_pokemon_than(identifier: Union[int, str]):
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
