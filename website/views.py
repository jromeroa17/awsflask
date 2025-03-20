from flask import Blueprint, request, flash
from flask import render_template

ec2 = boto3.client('ec2')
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/createInstance', methods=['GET','POST'])
def create_instance():
    if request.method == "POST":
        name = request.form.get('instanceName')
        opsys = request.form.get('so')
        keypair = request.form.get('keypair')
        instnum = request.form.get('instnum')

        flash(f'{name}: {opsys} la clave es {keypair} y hay que crear {instnum}')

    return render_template('createInstance.html')