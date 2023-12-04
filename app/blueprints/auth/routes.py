from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from ..forms import RegisterForm, LoginForm
from ..models import User

auth = Blueprint(name='auth', import_name=__name__, template_folder='auth_templates')

@auth.get('/register')
@auth.post('/register')
def register():
    form = RegisterForm()
    kwargs = {
        'title': 'PokeBattle | Register',
        'form': form,
        'current_user': current_user
        }

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            check_username = User.query.filter_by(username=username).first()
            check_email = User.query.filter_by(email=email).first()
            if check_username:
                pass
            elif check_email:
                pass
            else:
                user = User(username, email, password)
                user.CREATE()
                return redirect(url_for('auth.login'))
    return render_template('register.html.j2',  **kwargs)


@auth.get('/login')
@auth.post('/login')
def login():
    form = LoginForm()
    kwargs = {
        'title': 'PokeBattle | Login',
        'form': form,
        'current_user': current_user
    }

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    if 'next' in request.args:
                        return redirect(request.args['next'])
                    else:
                        return redirect(url_for('home.landing'))
                else:
                    return render_template('login.html.2')
            else:
                return render_template('login.html.j2')

    return render_template('login.html.j2', **kwargs)

@auth.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.landing'))