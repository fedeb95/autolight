from flask import Flask, render_template,request
from prova import Automation
import _thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/on/')
def light_on():
    aut.on()
    return render_template('index.html')

@app.route('/off/')
def light_off():
    aut.off()
    return render_template('index.html')

def flaskThread():
    app.run(host='0.0.0.0', port='80')

if __name__ == '__main__':
    aut = Automation()
    _thread.start_new_thread(flaskThread,())
    aut.run()
