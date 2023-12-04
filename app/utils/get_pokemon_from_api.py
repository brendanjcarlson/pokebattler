import requests

def get_pokemon_from_api(identifier):
    if identifier is None or not isinstance(identifier, (int, str)):
        return None
    
    url = f'https://pokeapi.co/api/v2/pokemon/{identifier}'
    response = requests.get(url)

    if response.ok:
        data = response.json()
        
        poke = {
            'game_id': data.get("id"),
            'name': data.get("name"),
            'weight': data.get("weight"),
            'height': data.get("height"),
            'stats': {s['stat']['name']: s['base_stat'] for s in data.get('stats')} if data.get('stats') is not None else {},
            'types': [t['type']['name'] for t in data.get('types')] if data.get('types') is not None else [],
            'sprites': {key: value for key, value in data.get('sprites').items() if value is not None and not isinstance(value, dict)} if data.get('sprites') is not None else {},
            'experience': data.get('base_experience'),
            }
        
    
        return poke
    else:
        return None