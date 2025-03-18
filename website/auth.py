from flask import Blueprint, request, flash
from flask import render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET","POST"])
def login():

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'

@auth.route('/sign-in', methods=["GET","POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4 or '@' not in email:
            flash("Email no válido o demasiado corto", category='error')
        elif len(username) < 8:
            flash("El nombre de usuario tiene menos de 8  caracteres", category='error')
        elif len(password1) < 8:
            flash("Contraseña demasiado corta", category='error')
        elif password2 != password1:
            flash("Contraseñas no coinciden", category='error')
        else:
            flash("Cuenta creada :)", category='success')
            # Añadir usuario lo hago mañana

    return render_template('signin.html')

