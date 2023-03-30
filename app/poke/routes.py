from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user, login_required
from ..forms import PokemonForm, UserForm
from ..helpers import get_pokemon_from_API
from ..models import Pokemon, User
from random import shuffle
from ..battle_logic import BattleGame

poke = Blueprint('poke', __name__, template_folder='poke_templates')


@poke.get('/search')
@poke.post('/search')
@login_required
def search():
    pokeform = PokemonForm()
    userform = UserForm()
    kwargs = {
        'title': 'PokeBattle | Search',
        'current_user': current_user,
        'pokeform': pokeform,
        'userform': userform,
    }
    if request.method == 'POST':
        if pokeform.validate():
            query = pokeform.pokemon.data

            try:
                query = int(query)
                poke = Pokemon.query.filter_by(poke_id=query).first()
            except:
                query = query.lower()
                poke = Pokemon.query.filter_by(name=query).first()

            if poke:
                print('\n\n✅✅FROM DB✅✅\n\n')
                poke = poke.TO_DICT()
            else:
                poke = get_pokemon_from_API(query)
                print('\n\n🚨🚨API CALLED🚨🚨\n\n')
                if poke:
                    new_poke = Pokemon(*poke.values())
                    new_poke.CREATE()
                    print('✅✅SAVED TO DB✅✅\n\n')

            if poke:
                kwargs['title'] = 'Results for {}'.format(poke['name'].title())
                kwargs['poke'] = poke
            else:
                kwargs['title'] = 'Pokemon not found'
            return render_template('search.html.j2', **kwargs)

    return render_template('search.html.j2', **kwargs)


@poke.get('/catch/<int:poke_id>')
@login_required
def catch(poke_id):
    kwargs = {
        'current_user': current_user,
        'username': current_user.username,
    }

    poke = Pokemon.query.filter_by(poke_id=poke_id).first()
    if not poke.is_caught and len(current_user.caught.all()) < 5:
        current_user.CATCH(poke)
        poke.is_caught = True
        poke.caught_by = current_user.username
        poke.UPDATE()
    return redirect(url_for('user.team', **kwargs))


@poke.get('/release/<int:poke_id>')
@login_required
def release(poke_id):
    kwargs = {
        'current_user': current_user,
        'username': current_user.username,
    }
    poke = Pokemon.query.filter_by(poke_id=poke_id).first()
    if poke in current_user.caught:
        current_user.RELEASE(poke)
        poke.is_caught = False
        poke.caught_by = None
        poke.UPDATE()
    return redirect(url_for('user.team', **kwargs))


@poke.get('/find-battle')
@login_required
def find_battle():
    pokeform = PokemonForm()
    userform = UserForm()
    kwargs = {
        'title': 'PokeBattle | Find Battle',
        'current_user': current_user,
        'userform': userform,
        'pokeform': pokeform,
    }

    battle_users = User.query.filter(User.username != current_user.username).all()
    if battle_users:
        shuffle(battle_users)
        battle_users = battle_users[:5]
        kwargs['battle_users'] = battle_users
    return render_template('find_battle.html.j2', **kwargs)

@poke.get('/battle/<string:username>')
@login_required
def battle(username):
    userform = UserForm()
    pokeform = PokemonForm()
    kwargs = {
        'title': 'PokeBattle | Battle Results',
        'userform': userform,
        'pokeform': pokeform,
        'winner': None,
        'loser': None,
        'log': None
    }
    opponent = User.query.filter_by(username=username).first()
    battle_game = BattleGame(current_user, opponent)
    kwargs['winner'], kwargs['loser'], kwargs['log'] = battle_game.battle()
    return render_template('battle_results.html.j2', **kwargs)