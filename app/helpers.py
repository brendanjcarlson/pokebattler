import requests
def get_pokemon_from_API(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        poke = {
            'id': data['id'],
            'name': data['name'],
            'types': ' '.join([t['type']['name'] for t in data['types']]),
            'abilities': ' '.join([a['ability']['name'] for a in data['abilities']]),
            'base_hp': data['stats'][0]['base_stat'],
            'base_atk': data['stats'][1]['base_stat'],
            'base_def': data['stats'][2]['base_stat'],
            'base_spd': data['stats'][5]['base_stat'],
            'base_exp': data['base_experience'],
            'height': data['height'],
            'weight': data['weight'],
            'sprite_url': data['sprites']['front_default'],
        }
        return poke
    else:
        return None