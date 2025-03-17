from flask import Blueprint
from flask import render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return '<h1>Home</h1>'

