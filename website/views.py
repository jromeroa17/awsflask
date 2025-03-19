from flask import Blueprint
from flask import render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/createInstance', methods=['GET','POST'])
def create_instance():
    return render_template('createInstance.html')