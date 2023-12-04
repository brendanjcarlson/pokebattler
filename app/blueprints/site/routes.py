from flask import render_template
from app.blueprints.site import site

# @home.get('/')
# def landing():
#     pokeform = PokemonForm()
#     userform = UserForm()
#     kwargs = {
#         'title': 'PokeBattle',
#         'current_user': current_user,
#         'pokeform': pokeform,
#         'userform': userform,
#     }
#     return render_template('landing.html.j2', **kwargs)

@site.get("/")
def index():
    return render_template("site/index.html")