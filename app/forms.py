from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class GMSHForm(Form):
    angle_start = IntegerField('angle_start')
    angle_stop = IntegerField('angle_stop')
    angles = IntegerField('angles')
    nodes = IntegerField('nodes')
    levels = IntegerField('levels')

#To run the code do "nr of samples", viscocity speed time file
#./airfoil num_samples visc speed T mesh.xml

class AirfoilForm(Form):
    samples = IntegerField('samples')
    viscocity = IntegerField('viscocity')
    speed = IntegerField('angles')
    time = IntegerField('time')
    filename = IntegerField('filename')
