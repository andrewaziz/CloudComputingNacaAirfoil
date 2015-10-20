# -*- coding: utf-8 -*-
import subprocess

from celery import Celery
from app import celery

# celery -A app.celery worker

@celery.task
def start_gmsh(angle_start, angle_stop, angles, nodes, levels):
	### FIX THIS
	subprocess.call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])
    subprocess.call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    subprocess.call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

@celery.task
def convert_msh(filename):
	filename_xml = filename[:-3]
	filename_xml += 'xml'
	subprocess.call(['sudo', 'dolfin-convert', filename, filename_xml])

@celery.task
def start_airfoil(samples, viscocity, speed, time, filename):
	filename = '/home/ubuntu/msh/{}'.format(filename)
	subprocess.call(['/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
					 samples, viscocity, speed, time, filename])
