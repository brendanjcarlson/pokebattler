from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user, login_required
from ..helpers import get_pokemon_from_API
from ..models import Pokemon, Caught, User
from ..forms import PokemonForm

user = Blueprint('user', __name__, template_folder='user_templates')

@user.get('/team/<string:username>')
@login_required
def team(username):
    form = PokemonForm()
    team = []
    kwargs = {
        'title': f'PokeBattle | {current_user.username}\'s Team',
        'user': current_user,
        'form': form,
        'pokemans': team
    }
    caught = Caught.query.filter_by(user_id=current_user.id).all()
    for poke in caught:
        poke = Pokemon.query.filter_by(poke_id=poke.poke_id).first()
        team.append(poke)
    return render_template('team.html.j2', **kwargs)


@user.get('/find_opponent')
@user.post('/find_opponenet')
@login_required
def find_opponenet():
    return '/user/find_opponent'