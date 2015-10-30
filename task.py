# -*- coding: utf-8 -*-
from subprocess import call, check_call, CalledProcessError
from celery import Celery
from app import celery, conn, git_dir, container
#from converter import makePlot # arg0 = path+.m-file, arg2 = path to storage
import time
import os
import os.path
import uuid


@celery.task
def gmsh_convert_airfoil(angle_start, angle_stop, angles, nodes, levels,
                         samples, viscocity, speed, time_step):
    ''' gmsh_convert_airfoil run gmsh with arguments then converts the .msh
        files created by gmsh to .xml with fenics dolfin. The xml files are
        passed as a argument to naca_airfoil. naca_airfoil run once for each
        level and each time produces a drag_ligt.m file. All xml and
        drag_ligt.m files are uploaded to the container specified in config.

    Args:
        angle_start (str) : smallest anglemof attack (degrees)
        angle_stop (str) : biggest angle of attack (degrees)
        angles (str) : split angle_stop - angle_start into angles parts
        nodes (str) : number of nodes on one side of airfoil
        levels (str) : number of refinement steps in meshing
            0=no refinement 1=one time 2=two times etc...
        samples (str) : number of samples saved
        viscocity (str) : the air's viscosity
        speed (str) : movement speed of wing
        time (str) : total amount of time

    Returns:
        None

    '''
    os.chdir(git_dir)
    try:
        call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])

    except CalledProcessError as e:
        print e
        
    call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

    for level in range(int(levels) + 1):
        path = '/home/ubuntu/msh/'
        filename = '/home/ubuntu/msh/r{}a{}n{}.msh'.format(level, angle_start, nodes)
        filename_xml = filename[:-3]
        filename_xml += 'xml'
       	try:
	    check_call('sudo dolfin-convert {} {}'.format(filename, filename_xml), shell=True)
	except CalledProcessError as e:
	    print e
        with open(filename_xml) as f:
            conn.put_object(container, filename_xml[len(path):],
                            contents=f.read(), content_type='text/plain')

    airfoil_path = '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil'
    for level in range(int(levels) + 1):
        u = str(uuid.uuid4())
        root_dir = '/home/ubuntu'
        result_dir = '{}/r{}a{}n{}/{}'.format(root_dir, level, angle_start, nodes, u)

        filename_xml = '/home/ubuntu/msh/r{}a{}n{}.xml'.format(level, angle_start, nodes)


        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        os.chdir(result_dir)

        try:
            check_call(['sudo', '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
         	            samples, viscocity, speed, time_step, filename_xml])

        except CalledProcessError as e:
            print e

        filename = '{}/s{}v{}s{}t{}/drag_lift.m'.format(filename_xml[len(path):], samples, viscocity, speed, time_step)

        result_file = '{}/results/drag_ligt.m'.format(result_dir)
        
        call('sudo python /home/ubuntu/test/converter.py {}'.format(result_file) + " {}".format(result_dir), shell=True)
        
        try:
            with open(result_file) as f:
                conn.put_object(container, filename,
                                contents=f.read(), content_type='text/plain')
            with open(result_dir + '/plot_lift.png') as f:
                conn.put_object(container, filename[:-11]+"plot_lift.png",
                                contents=f.read(), content_type='text/plain')
            with open(result_dir + '/plot_drag.png') as f:
                conn.put_object(container, filename[:-11]+"plot_drag.png",
                                contents=f.read(), content_type='text/plain')
        except IOError as e:
            print e


@celery.task
def start_gmsh(angle_start, angle_stop, angles, nodes, levels):
    ''' start_gmsh run gmsh with arguments then converts the .msh
        files created by gmsh to .xml with fenics dolfin. One .xml file is
        uploaded for every level.

    Args:
        angle_start (str) : smallest anglemof attack (degrees)
        angle_stop (str) : biggest angle of attack (degrees)
        angles (str) : split angle_stop - angle_start into angles parts
        nodes (str) : number of nodes on one side of airfoil
        levels (str) : number of refinement steps in meshing
            0=no refinement 1=one time 2=two times etc...

    Returns:
        None
    '''
    os.chdir(git_dir)
    try:
        call(['./run.sh', angle_start, angle_stop, angles, nodes, levels])
    except CalledProcessError as e:
        print e

    call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)

    for level in range(int(levels) + 1):
        path = '/home/ubuntu/msh/'
        filename = '/home/ubuntu/msh/r{}a{}n{}.msh'.format(level, angle_start, nodes)
        filename_xml = filename[:-3]
        filename_xml += 'xml'
        try:
            check_call('sudo dolfin-convert {} {}'.format(filename, filename_xml), shell=True)
        except CalledProcessError as e:
            print e

        try:
            with open(filename_xml) as f:
                conn.put_object(container, filename_xml[len(path):],
                                contents=f.read(), content_type='text/plain')
        except IOError as e:
            print e


@celery.task
def start_airfoil(samples, viscocity, speed, time_step, filename):
    ''' Start_airfoil runs naca_airfoil with supplied arguments and uploads the
    created file by naca_airfoil drag_ligt.m to the container specified in
    config.

    Args:
        samples (str) : number of samples saved
        viscocity (str) : the air's viscosity
        speed (str) : movement speed of wing
        time (str) : total amount of time
        filename (str): xml file served to naca_airfoil

    Returns:
        None

    '''
    call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)
    os.chdir(git_dir)
    filename_path = '/home/ubuntu/msh/{}'.format(filename)

    if not os.path.exists(filename_path):
        os.chdir('/home/ubuntu/msh')
	response, data = conn.get_object(container, filename)
        filename_path = filename
    	call('sudo chown -R ubuntu /home/ubuntu/msh', shell=True)
    	call('sudo chown -R ubuntu /home/ubuntu/geo', shell=True)
        with open(filename, 'w') as f:
            f.write(data)
	os.chdir(git_dir)
    airfoil_path = '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil'

    
    u = str(uuid.uuid4())
    root_dir = '/home/ubuntu'
    result_dir = '{}/{}/{}'.format(root_dir, filename[:-4], u)
    if not os.path.exists(result_dir):
	os.makedirs(result_dir)    
	
    os.chdir(result_dir)

    
    try:
        check_call(['sudo', '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
         	    samples, viscocity, speed, time_step, filename_path])

    except CalledProcessError as e:
        print e

    object_name = '{}/s{}v{}s{}t{}/drag_lift.m'.format(filename,
                                        samples, viscocity, speed, time_step)

    plot_path = '{}/s{}v{}s{}t{}'.format(filename,
                                        samples, viscocity, speed, time_step)

    result_file = '{}/results/drag_ligt.m'.format(result_dir)

    try:
  
        call('sudo python /home/ubuntu/test/converter.py {}'.format(result_file) + " {}".format(result_dir), shell=True)
        
        with open(result_file) as f:
            conn.put_object(container, object_name,
                            contents=f.read(), content_type='text/plain')
            with open(result_dir + '/plot_lift.png') as f:
                conn.put_object(container, object_name[:-11]+"plot_lift.png",
                                contents=f.read(), content_type='text/plain')
            with open(result_dir + '/plot_drag.png') as f:
                conn.put_object(container, object_name[:-11]+"plot_drag.png",
                                contents=f.read(), content_type='text/plain')
    except IOError as e:
        print e





