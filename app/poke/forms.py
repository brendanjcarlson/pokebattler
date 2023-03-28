from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemon = StringField('Enter a pokemon', validators=[DataRequired()], render_kw={"placeholder": "Search for a pokemon!"})
    submit = SubmitField('Search')