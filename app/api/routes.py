from flask import Blueprint
from ..models import Pokemon, User, db
from ..helpers import get_pokemon_from_API


api = Blueprint('api', __name__)


@api.get('user/<string:username>/team')
def team(username):
    user = User.poke_query.filter_by(username=username).first()
    if user:
        caught = user.caught.all()
        return {'status': 'ok', 'team': [poke.TO_DICT() for poke in caught]}
    return {'status': 'not ok', 'message': 'user not found'}


@api.get('poke/<poke_query>')
def poke_name(poke_query):
    try:
        poke_query = int(poke_query)
        poke = Pokemon.query.filter_by(poke_id=poke_query).first()
    except:
        poke_query = poke_query.lower()
        poke = Pokemon.query.filter_by(name=poke_query).first()

    if poke:
        print('\n\n✅✅ FROM DB ✅✅\n\n')
        poke = poke.TO_DICT()
    else:
        poke = get_pokemon_from_API(poke_query)
        print(f"\n\n🚨🚨 API CALLED for {poke_query} 🚨🚨\n\n")
        if poke:
            new_poke = Pokemon(*poke.values())
            new_poke.CREATE()
            print('✅✅ SAVED TO DB ✅✅\n\n')

    if poke:
        return {'status': 'ok', 'poke': poke}
    return {'status': 'not ok', 'message': 'poke not found'}