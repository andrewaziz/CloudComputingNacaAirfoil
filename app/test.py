from flask import send_file
from flask import Flask
from flask import url_for, redirect

app = Flask(__name__)

@app.route('/')
def get_image():
    filename = 'plot_lift.png'
    return send_file(filename, mimetype='image/png')
    
@app.route('/a')
def get_info():
    #return redirect('./tmp.html')
    return redirect(url_for('static', filename='tmp.html'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')





