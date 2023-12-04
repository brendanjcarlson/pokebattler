from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.blueprints.auth import auth
from app.blueprints.auth.forms import LoginForm, RegisterForm
from app.models import User



@auth.get("/register")
def view_register():
    if current_user.is_authenticated:
        return redirect(url_for('site.view_index'))

    form = RegisterForm()

    return render_template('auth/views/register.html', form=form)



@auth.post("/register")
def handle_register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        try:
            # TODO Add route param on error
            if User.query.filter_by(email=email).first():
                return redirect(url_for('auth.view_register'))

            if User.query.filter_by(username=username).first():
                return redirect(url_for('auth.view_register'))

            user = User(email=email, username=username, password=password)
            user.save()
        except:
            return redirect(url_for('auth.view_register'))

        return redirect(url_for('auth.view_login'))



@auth.get("/login")
def view_login():
    if current_user.is_authenticated:
        return redirect(url_for('site.view_index'))
    
    form = LoginForm()

    return render_template('auth/views/login.html', form=form)



@auth.post("/login")
def handle_login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        identity = form.identity.data
        password = form.password.data

        try:
            email_user = User.query.filter_by(email=identity).first()
            username_user = User.query.filter_by(username=identity).first()

            if not email_user and not username_user:
                return redirect(url_for('auth.view_login'))

            if email_user:
                user = email_user
            else:
                user = username_user

            if not user.check_password(password):
                return redirect(url_for('auth.view_login'))

            user.login()
            return redirect(url_for('site.view_index'))
            
        except:
            return redirect(url_for('auth.view_login'))


@auth.get('/logout')
@login_required
def handle_logout():
    current_user.logout()

    return redirect(url_for('site.view_index'))