import os
import swiftclient.client
from celery import Celery
from flask import Flask

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

git_dir = '/home/ubuntu/test'
container = os.environ['OS_CONTAINER']

conf = {'user':os.environ['OS_USERNAME'],
        'key':os.environ['OS_PASSWORD'],
        'tenant_name':os.environ['OS_TENANT_NAME'],
        'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **conf)


celery = Celery('task', backend='amqp',
                broker='amqp://{}:password@{}:5672/host'.format
                (os.environ['worker_id'], os.environ['controller_ip']))

celery.conf.update(app.config)


from app import views
