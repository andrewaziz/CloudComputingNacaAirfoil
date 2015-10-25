# -*- coding: utf-8 -*-
import subprocess

from celery import Celery
from app import celery
from app import conn
# celery -A app.celery worker

@celery.task
def gmsh_convert_airfoil(angle_start, angle_stop, angles, nodes, levels):
    subprocess.call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])
    subprocess.call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    subprocess.call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

    for level in range(int(levels) + 1):
        path = '/home/ubuntu/msh/'
        filename = '/home/ubuntu/msh/r{}a{}n{}.msh'.format(level, angle_start, nodes)
        filename_xml = filename[:-3]
        filename_xml += 'xml'
        subprocess.check_call('sudo dolfin-convert {} {}'.format(filename, filename_xml), shell=True)

        with open(filename_xml) as f:
            conn.put_object('g17container', filename_xml[len(path):],
                            contents=f.read(), content_type='text/plain')

        airfoil_path = '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil'
        subprocess.check_call('sudo {} {} {} {} {} {}'.format(airfoil_path,
                    samples, viscocity, speed, time, filename), shell=True)


        filename = '{}/drag_lift.m'.format(filename_xml[len(path):])
        with open('/results/drag_lift.m') as f:
            conn.put_object('g17container', filename,
                            contents=f.read(), content_type='text/plain')



@celery.task
def start_gmsh(angle_start, angle_stop, angles, nodes, levels):
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
	subprocess.call(['sudo', '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
					 samples, viscocity, speed, time, filename])
