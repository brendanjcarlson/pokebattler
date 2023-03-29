from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    pokemon = StringField('Search for a pokemon!', validators=[DataRequired()], render_kw={'placeholder': 'Search for a pokemon!'})
    submit = SubmitField('Search')