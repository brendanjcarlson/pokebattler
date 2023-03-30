from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user, login_required
from ..helpers import get_pokemon_from_API
from ..models import Pokemon, User
from ..forms import PokemonForm, UserForm

user = Blueprint('user', __name__, template_folder='user_templates')

@user.get('/<string:username>/team')
@login_required
def team(username):
    pokeform = PokemonForm()
    userform = UserForm()
    kwargs = {
        'title': f'PokeBattle | {current_user.username}\'s Team',
        'current_user': current_user,
        'display_user': current_user,
        'pokeform': pokeform,
        'userform': userform,
        'pokemans': []
    }

    if username != current_user.username:
        user = User.query.filter_by(username=username).first()
        if user:
            kwargs['display_user'] = user
            kwargs['title'] = f'PokeBattle | {user.username}\'s Team'
    for poke in kwargs['display_user'].caught.all():
        kwargs['pokemans'].append(poke.TO_DICT())
    return render_template('team.html.j2', **kwargs)


@user.get('/search')
@user.post('/search')
@login_required
def search():
    pokeform = PokemonForm()
    userform = UserForm()
    kwargs = {
        'title': f'PokeBattle | Search',
        'current_user': current_user,
        'pokeform': pokeform,
        'userform': userform,
    }

    if request.method == 'POST':
        if userform.validate():
            found_user = User.query.filter_by(username=userform.user.data).first()
            if found_user:
                return redirect(url_for('user.team', username=found_user.username))

    return render_template('search.html.j2', **kwargs)