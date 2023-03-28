from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user

home = Blueprint('home', __name__, template_folder='home_templates')

@home.get('/')
def home_page():
    title = 'PokeBattle'
    return render_template('home.html.j2', title=title, user=current_user)