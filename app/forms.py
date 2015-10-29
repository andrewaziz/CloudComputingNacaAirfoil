from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class GMSHForm(Form):
    angle_start = IntegerField('angle_start')
    angle_stop = IntegerField('angle_stop')
    angles = IntegerField('angles')
    nodes = IntegerField('nodes')
    levels = IntegerField('levels')


class GMSHAirfoilForm(Form):
    angle_start = StringField('angle_start')
    angle_stop = StringField('angle_stop')
    angles = StringField('angles')
    nodes = StringField('nodes')
    levels = StringField('levels')

    samples = StringField('samples')
    viscocity = StringField('viscocity')
    speed = StringField('angles')
    time_step = StringField('time_step')


class AirfoilForm(Form):
    samples = StringField('samples')
    viscocity = StringField('viscocity')
    speed = StringField('angles')
    time_step = StringField('time_step')
    filename = StringField('filename')
