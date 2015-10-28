
from flask import send_file
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    file = open("result.txt", "r")
    lines = file.readlines()
    return lines[0]

@app.route('/plot')
def get_image():
#    if request.args.get('type') == '1':
    #filename = '/home/hampus/skola/CloudComputing/FilesFromAssignments2015-09-15/C3/app/plot.png'
    filename = 'plot.png'
    return send_file(filename, mimetype='image/png')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')

