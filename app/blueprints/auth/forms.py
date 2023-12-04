from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length



class RegisterForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[InputRequired(),
                                       Length(min=3, max=16, message="Username must be between 3 and 16 characters")],
                           render_kw={"placeholder": "Username"})

    email = StringField(label='Email',
                        validators=[InputRequired()],
                        render_kw={"placeholder": "Email"})

    password = PasswordField(label='Password',
                             validators=[InputRequired(), Length(min=8)], 
                             render_kw={"placeholder": 'Password'})

    confirm_password = PasswordField(label='Confirm password', 
                                    validators=[InputRequired(), EqualTo('password')], 
                                    render_kw={"placeholder": 'Confirm password'})
    
    submit = SubmitField(label='Register')



class LoginForm(FlaskForm):
    username = StringField(label='Username', 
                           validators=[InputRequired()], 
                           render_kw={"placeholder": "Username"})

    password = PasswordField(label='Password', 
                             validators=[InputRequired()], 
                             render_kw={"placeholder": 'Password'})

    submit = SubmitField(label='Login')