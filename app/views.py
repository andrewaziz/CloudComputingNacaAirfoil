# -*- coding: utf-8 -*-
import glob
import subprocess
from celery import group, subtask
from flask import render_template, make_response, redirect, request
from app import app, container
from .forms import GMSHForm, GMSHAirfoilForm, AirfoilForm
from task import start_gmsh, start_airfoil, gmsh_convert_airfoil
import urllib2
from flask import send_file

import os
from sys import argv
import time
from novaclient.client import Client
import uuid
import swiftclient.client
        

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/result')
def gset_image():
    result = ""

    config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
    
    conn = swiftclient.client.Connection(auth_version=2, **config)

    container_name = "g17container"
    tmp = conn.get_container(container_name)
    for num in range(0,len(tmp[1])):
        item = tmp[1][num]['name']
        result = result + '<a href="http://smog.uppmax.uu.se:8080/swift/v1/g17container/' + item  + '" rel="nofollow">' + item + '</a> <br> '
    return(result)
                
@app.route('/gmshairfoil', methods=['GET', 'POST'])
def test():
    form = GMSHAirfoilForm()
    if form.validate_on_submit():
        angle_start = int(form.angle_start.data)
        angle_stop = int(form.angle_stop.data)
        angles = int(form.angles.data)
        nodes = form.nodes.data
        levels = form.levels.data
        samples = form.samples.data
        viscocity = form.viscocity.data
        speed = form.angles.data
        time_step = form.time_step.data
        step = ((angle_stop - angle_start) / angles)

	# We create a list with angles to run with gmsh, gmsh get called
	# with same value for angle_start and angle_stop to guarantee that gmsh
	# only produces one .msh file for each call.

	angle_list = [angle_start + step*x for x in range(angles+1)]

        res = group([gmsh_convert_airfoil.s(str(x), str(x), str(angles),
                        nodes, levels, samples,viscocity,
                        speed, time_step) for x in angle_list])()

        
        return render_template('gmshairfoil.html', form=form)

    return render_template('gmshairfoil.html', form=form)


@app.route('/gmsh', methods=['GET', 'POST'])
def gmsh():
	form = GMSHForm()
	if form.validate_on_submit():
		angle_start = int(form.angle_start.data)
		angle_stop = int(form.angle_stop.data)
		angles = int(form.angles.data)
		nodes = str(form.nodes.data)
		levels = str(form.levels.data)
		step = ((angle_stop - angle_start) / angles)
		angle_list = [angle_start + step*x for x in range(angles+1)]
		res = group([start_gmsh.s(str(x), str(x), str(angles), nodes, levels) for x in angle_list])
		res()

		return redirect('/index')

	return render_template('gmsh.html', form=form)

@app.route('/airfoil', methods=['GET', 'POST'])
def airfoil():
	form = AirfoilForm()
	if form.validate_on_submit():
		samples = form.samples.data
		viscocity = form.viscocity.data
		speed = form.speed.data
		time_step = form.time_step.data
		filename = form.filename.data
		start_airfoil.delay(samples, viscocity, speed, time_step, filename)


		return redirect('/index')


	return render_template('airfoil.html', form=form)



@app.route('/api/v1.0/<xml>', methods=['GET'])
def get_xml_file(xml):
	url = 'http://smog.uppmax.uu.se:8080/swift/v1/{}/{}'.format(container, xml)
	data = urllib2.urlopen(url)

	response = make_response(data.read())
	response.headers["Content-Disposition"] = "attachment; filename={}".format(xml)

	return response

@app.route('/api/v1.0/<xml>/<settings>/<f>', methods=['GET'])
def get_draglift(xml, settings, f):
	url = 'http://smog.uppmax.uu.se:8080/swift/v1/{}/{}/{}/{}'.format(container, xml, settings, f)
	data = urllib2.urlopen(url)

	response = make_response(data.read())
	response.headers["Content-Disposition"] = "attachment; filename={}".format(f)

	return response
