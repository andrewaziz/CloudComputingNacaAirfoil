# -*- coding: utf-8 -*-
import glob
import subprocess
from celery import group, subtask
from flask import render_template, make_response, redirect, request
from app import app
from .forms import LoginForm, GMSHForm, AirfoilForm
from task import start_gmsh, convert_msh, start_airfoil

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Bob'}
	return render_template('index.html', title='Home', user=user)

@app.route('/gmsh', methods=['GET', 'POST'])
def gmsh():
	form = GMSHForm()
	if form.validate_on_submit():
		angle_start = str(form.angle_start.data)
		angle_stop = str(form.angle_stop.data)
		angles = str(form.angles.data)
		nodes = str(form.nodes.data)
		levels = str(form.levels.data)

		res = start_gmsh.delay(angle_start, angle_stop, angles, nodes, levels)
		res.get()

		files = glob.glob('/home/ubuntu/msh/*.msh')
		convert_group = group([convert_msh.s(msh) for msh in files])
		res = convert_group()

		return redirect('/index')

	return render_template('gmsh.html', form=form)

@app.route('/airfoil', methods=['GET', 'POST'])
def airfoil():
	form = AirfoilForm()
	if form.validate_on_submit():
		samples = str(form.samples.data)
		viscocity = str(form.viscocity.data)
		speed = str(form.angles.data)
		time = str(form.time.data)
		filename = str(form.filename.data)

		start_airfoil.delay(samples, viscocity, speed, time, filename)


		return redirect('/index')


	return render_template('airfoil.html', form=form)



@app.route('/convert', methods=['POST'])
def convert():
	if not request.json or 'convert' not in request.json:
		abort(400)

	files = glob.glob('/home/ubuntu/msh/*.msh')
	file = '/home/ubuntu/msh/{}'.format(request.json['convert'])
	print file
	print request.json['convert']
	if request.json['convert'] == 'all':
		convert_group = group([convert_msh.s(msh) for msh in files])
		res = convert_group()

	elif file in files:
		convert_msh.delay(file)

	return redirect('/index')




### SERVE FILE EXAMPLE
@app.route("/api/air", methods=["GET"])
def get_air():

    with open("/Users/niklas/GitHub/test/geo/geo.txt", "r+") as f:
        data = f.read()

    response = make_response(data)

    response.headers["Content-Disposition"] = "attachment; filename=data.txt"
    return response
