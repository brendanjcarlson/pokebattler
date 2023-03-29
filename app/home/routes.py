from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user
from ..forms import PokemonForm

home = Blueprint('home', __name__, template_folder='home_templates')

@home.get('/')
def landing():
    form = PokemonForm()
    kwargs = {
        'title': 'PokeBattle',
        'user': current_user,
        'form': form
    }
    return render_template('landing.html.j2', **kwargs)