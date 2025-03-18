from flask import Blueprint
from flask import render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'

@auth.route('/sign-in')
def sign_in():
    return render_template('signin.html')

