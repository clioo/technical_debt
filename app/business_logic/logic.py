from fcntl import DN_DELETE
from this import d
from providers import poke as poke_provider
from typing import Dict, Optional, Union


def get_pokemon_stat(pokemon_data: dict, required_stat: str) -> int:
    for stat in pokemon_data.get("stats", []):
        if stat.get("stat").get("name") == required_stat:
            return stat.get("base_stat")
    raise Exception("[1002] No stat name found in that pokemon.")


def get_stronger_pokemon_than(identifier: Union[str, int]) -> Optional[Dict]:
    my_pokemon_data = poke_provider.get_pokemon(identifier=identifier)
    my_pokemon_attack = get_pokemon_stat(my_pokemon_data, required_stat="attack")
    offset = 0
    pokemons = poke_provider.get_pokemons(offset=offset)
    while pokemons:
        for pokemon_data in pokemons:
            pokemon_full_stats = poke_provider.get_pokemon(
                identifier=pokemon_data.get("name")
            )
            challenger_value = get_pokemon_stat(
                pokemon_full_stats, required_stat="attack"
            )
            if challenger_value > my_pokemon_attack:
                return pokemon_data
        # Next pokemon page
        offset += 20
        pokemons = poke_provider.get_pokemons(offset=offset)
