from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemon = StringField('Search for a pokemon!', validators=[DataRequired()], render_kw={'placeholder': 'Search for a pokemon!'})
    submit = SubmitField('Search')

class UserForm(FlaskForm):
    user = StringField('Search for a user!', validators=[DataRequired()], render_kw={'placeholder': 'Search for an opponent!'})
    submit = SubmitField('Search')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": 'Password'})
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": 'Confirm password'})
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": 'Password'})
    submit = SubmitField('Login')