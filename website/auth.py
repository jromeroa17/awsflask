from flask import Blueprint, request, flash, redirect, url_for
from flask import render_template
from .models import Usuario
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')

        user = Usuario.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password")

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully")
    return redirect(url_for('auth.login'))

@auth.route('/sign-in', methods=["GET","POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Usuario.query.filter_by(username=username).first()

        if user:
            print("Cuenta ya existe para ese usuario")
        elif len(email) < 4 or '@' not in email:
            flash("Email no válido o demasiado corto", category='error')
        elif len(username) < 8:
            flash("El nombre de usuario tiene menos de 8  caracteres", category='error')
        elif len(password1) < 8:
            flash("Contraseña demasiado corta", category='error')
        elif password2 != password1:
            flash("Contraseñas no coinciden", category='error')
        else:
            new_user = Usuario(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash("Cuenta creada :)", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('signin.html', user=current_user)

