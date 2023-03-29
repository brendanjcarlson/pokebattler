from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user, login_required
from ..forms import PokemonForm
from ..helpers import get_pokemon_from_API
from ..models import Pokemon, Caught, User

poke = Blueprint('poke', __name__, template_folder='poke_templates')


@poke.get('/search')
@poke.post('/search')
@login_required
def search():
    form = PokemonForm()
    kwargs = {
        'title': 'PokeBattle | Search',
        'user': current_user,
        'form': form,
    }
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
                    kwargs['caught_user'] = caught_user
                    kwargs['caught'] = caught
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
def catch(poke_id):
    caught = Caught.query.filter_by(user_id=current_user.id).all()
    if len(caught) >= 5:
        return redirect(url_for('poke.search'))
    not_available = Caught.query.filter_by(poke_id=poke_id).first()
    if not_available:
        return redirect(url_for('poke.search'))
    else:
        caught = Caught(current_user.id, poke_id)
        caught.CREATE()
    return redirect(url_for('poke.search'))


@poke.get('/release/<int:poke_id>')
def release(poke_id):
    caught = Caught.query.filter_by(user_id=current_user.id, poke_id=poke_id).first()
    caught.DELETE()
    return redirect(url_for('user.team', username=current_user.username, user=current_user))
