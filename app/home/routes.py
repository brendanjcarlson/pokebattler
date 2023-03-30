from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user
from ..forms import PokemonForm, UserForm

home = Blueprint('home', __name__, template_folder='home_templates')

@home.get('/')
def landing():
    pokeform = PokemonForm()
    userform = UserForm()
    kwargs = {
        'title': 'PokeBattle',
        'current_user': current_user,
        'pokeform': pokeform,
        'userform': userform,
    }
    return render_template('landing.html.j2', **kwargs)