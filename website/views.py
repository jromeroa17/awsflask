from flask import Blueprint, request, flash
from flask import render_template
import boto3
import botocore.exceptions


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

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/createInstance', methods=['GET','POST'])
def create_instance():
    if request.method == "POST":
        name = request.form.get('instanceName')
        opsys = request.form.get('so')
        keypair = request.form.get('keypair')
        instnum = int(request.form.get('instnum'))

        try:
            crearInstancia(name,opsys,keypair,instnum)
        except botocore.exceptions.ClientError:
            ec2.create_key_pair(KeyName=keypair)
            crearInstancia(name, opsys, keypair, instnum)

    return render_template('createInstance.html')

amis = {
    'AmazonLinux':'ami-08b5b3a93ed654d19',
    'Ubuntu':'ami-084568db4383264d4',
    'WinServer':'ami-02e3d076cbd5c28fa',
    'Debian':'ami-0779caf41f9ba54f0',
}

