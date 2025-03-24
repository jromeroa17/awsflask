from flask import Blueprint, request, flash
from flask import render_template
import boto3
import botocore.exceptions
from flask_login import login_required, current_user
from . import db

from .models import Instancia


ec2 = boto3.client('ec2')
views = Blueprint('views', __name__)

def crearInstancia(name,opsys,keypair,instnum):
    response = ec2.run_instances(
        ImageId=amis[opsys],
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=instnum,
        KeyName=keypair,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ]
            },
        ]
    )
    return response

def db_instancia(name,opsys,keypair):
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [name]}])['Reservations']
    instanceid = response[0]['Instances'][0]['InstanceId']
    new_instance = Instancia(id=instanceid,name=name, opsys=opsys, keypairs=keypair, user_id=current_user.id)
    db.session.add(new_instance)
    db.session.commit()


@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/createInstance', methods=['GET','POST'])
@login_required
def create_instance():
    if request.method == "POST":
        name = request.form.get('instanceName')
        opsys = request.form.get('so')
        keypair = request.form.get('keypair')
        instnum = int(request.form.get('instnum'))

        instance = Instancia.query.filter_by(name=name).first()

        if instance:
            flash("Instancia ya existe", category='error')
        else:
            try:
                crearInstancia(name,opsys,keypair,instnum)
                db_instancia(name,opsys,keypair)
                flash("Instancia Creada", category='success')
            except botocore.exceptions.ClientError:
                ec2.create_key_pair(KeyName=keypair)
                crearInstancia(name, opsys, keypair, instnum)
                db_instancia(name, opsys, keypair)
                flash("Instancia Creada", category='success')



    return render_template('createInstance.html', user=current_user)

@views.route('/misInstancias', methods=['GET','POST'])
@login_required
def mis_instancias():

    if request.method == 'POST':
        for Instancia in current_user.Instance:
            orden = request.form.get(f'orden{Instancia.name}')
            if orden == 'Iniciar':
                ec2.start_instances(InstanceIds=[Instancia.id])
                flash("Instancia Iniciada")
            elif orden == 'Parar':
                ec2.stop_instances(InstanceIds=[Instancia.id])
                flash("Instancia Parada")
    return render_template('misinstancias.html',  user=current_user)

amis = {
    'AmazonLinux':'ami-08b5b3a93ed654d19',
    'Ubuntu':'ami-084568db4383264d4',
    'WinServer':'ami-02e3d076cbd5c28fa',
    'Debian':'ami-0779caf41f9ba54f0',
}

