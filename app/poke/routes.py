from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user, login_required
from .forms import PokemonForm
from ..helpers import get_pokemon_from_API
from ..models import Pokemon, Caught, User

poke = Blueprint('poke', __name__, template_folder='poke_templates')


@poke.get('/search')
@poke.post('/search')
@login_required
def poke_search():
    form = PokemonForm()
    title = 'Search'
    if request.method == 'POST':
        if form.validate():
            query = form.pokemon.data
            poke = None
            caught = None
            caught_user = None

            try:
                query = int(query)
                poke = Pokemon.query.filter_by(poke_id=query).first()
            except:
                query = query.lower()
                poke = Pokemon.query.filter_by(name=query).first()

            if poke:
                print('\n\n✅✅FROM DB✅✅\n\n')
                caught = Caught.query.filter_by(poke_id=poke.poke_id).first()
                if caught:
                    caught_user = User.query.filter_by(id=caught.user_id).first()
                poke = poke.TO_DICT()
            else:
                poke = get_pokemon_from_API(query)
                print('\n\n🚨🚨API CALLED🚨🚨\n\n')
                if poke:
                    new_poke = Pokemon(*poke.values())
                    new_poke.CREATE()
                    print('✅✅SAVED TO DB✅✅\n\n')

            if poke:
                title = 'Results for {}'.format(poke['name'].title())
            else:
                title = 'Pokemon not found'
            return render_template('search.html.j2', title=title, form=form, user=current_user, poke=poke, caught=caught, caught_user=caught_user)

    return render_template('search.html.j2', title=title, form=form, user=current_user)


@poke.get('/catch/<int:poke_id>')
def poke_catch(poke_id):
    caught = Caught.query.filter_by(user_id=current_user.id).all()
    if len(caught) >= 5:
        return redirect(url_for('poke.poke_search'))
    not_available = Caught.query.filter_by(poke_id=poke_id).first()
    if not_available:
        return redirect(url_for('poke.poke_search'))
    else:
        caught = Caught(current_user.id, poke_id)
        caught.CREATE()
    return redirect(url_for('poke.poke_search'))


@poke.get('/release/<int:poke_id>')
def poke_release(poke_id):
    caught = Caught.query.filter_by(user_id=current_user.id, poke_id=poke_id).first()
    caught.DELETE()
    return redirect(url_for('poke.poke_team', username=current_user.username, user=current_user))


@poke.get('/team/<string:username>')
@login_required
def poke_team(username):
    form = PokemonForm()
    title = 'Team'
    caught = Caught.query.filter_by(user_id=current_user.id).all()
    pokemans = []
    for c in caught:
        poke = Pokemon.query.filter_by(poke_id=c.poke_id).first()
        pokemans.append(poke.TO_DICT())

    return render_template('team.html.j2', title=title, user=current_user, pokemans=pokemans, form=form, caught=False)