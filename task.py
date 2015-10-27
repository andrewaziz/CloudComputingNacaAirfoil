# -*- coding: utf-8 -*-
from subprocess import call, check_call, CalledProcessError
from celery import Celery
from app import celery
from app import conn
import time
import os.path

@celery.task
def gmsh_convert_airfoil(angle_start, angle_stop, angles, nodes, levels, samples, viscocity, speed, time_step):
    call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])
    call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

    for level in range(int(levels) + 1):
        path = '/home/ubuntu/msh/'
        filename = '/home/ubuntu/msh/r{}a{}n{}.msh'.format(level, angle_start, nodes)
        filename_xml = filename[:-3]
        filename_xml += 'xml'
       	check_call('sudo dolfin-convert {} {}'.format(filename, filename_xml), shell=True)

        with open(filename_xml) as f:
            conn.put_object('g17container', filename_xml[len(path):],
                            contents=f.read(), content_type='text/plain')

        airfoil_path = '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil'

	try:
		check_call(['sudo', '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
                    samples, viscocity, speed, time_step, filename_xml])

	except CalledProcessError as e:
		print e

	filename = '{}/s{}v{}s{}t{}/drag_lift.m'.format(filename_xml[len(path):],
                                        samples, viscocity, speed, time_step)

	with open('/home/ubuntu/test/results/drag_ligt.m') as f:
            conn.put_object('g17container', filename,
                            contents=f.read(), content_type='text/plain')



@celery.task
def start_gmsh(angle_start, angle_stop, angles, nodes, levels):
    call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])
    call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

    for level in range(int(levels) + 1):
        path = '/home/ubuntu/msh/'
        filename = '/home/ubuntu/msh/r{}a{}n{}.msh'.format(level, angle_start, nodes)
        filename_xml = filename[:-3]
        filename_xml += 'xml'
       	check_call('sudo dolfin-convert {} {}'.format(filename, filename_xml), shell=True)

        with open(filename_xml) as f:
            conn.put_object('g17container', filename_xml[len(path):],
                            contents=f.read(), content_type='text/plain')

@celery.task
def convert_msh(filename):
	filename_xml = filename[:-3]
	filename_xml += 'xml'
	call(['sudo', 'dolfin-convert', filename, filename_xml])

@celery.task
def start_airfoil(samples, viscocity, speed, time_step, filename):
    filename_path = '/home/ubuntu/msh/{}'.format(filename)

    if not os.path.exists(filename_path):
        response, data = conn.get_object('g17container', filename)
        filename_path = filename
        with open(filename, 'w') as f:
            f.write(data)

    airfoil_path = '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil'

    try:
        check_call(['sudo', '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
                    samples, viscocity, speed, time_step, filename_path])

    except CalledProcessError as e:
        print e

    object_name = '{}/s{}v{}s{}t{}/drag_lift.m'.format(filename,
                                        samples, viscocity, speed, time_step)

    with open('/home/ubuntu/test/results/drag_ligt.m') as f:
        conn.put_object('g17container', object_name,
                        contents=f.read(), content_type='text/plain')
