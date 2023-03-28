from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from .forms import RegisterForm, LoginForm
from ..models import User

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.get('/register')
@auth.post('/register')
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            check_username = User.query.filter_by(username=username).first()
            check_email = User.query.filter_by(email=email).first()
            if check_username:
                flash('username already in use')
            elif check_email:
                print('email already in use')
            else:
                user = User(username, email, password)
                user.CREATE()
                return redirect(url_for('auth.login_page'))
    return render_template('register.html.j2', form=form, user=current_user)


@auth.get('/login')
@auth.post('/login')
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home.home_page'))
                else:
                    print('invalid password')
                    return render_template('login.html.2')
            else:
                print('username does not exist')
                return render_template('login.html.j2')

    return render_template('login.html.j2', form=form, user=current_user)

@auth.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))