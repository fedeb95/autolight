from flask import Flask, render_template,request
from light_switch import LightSwitch
from threading import Thread


app = Flask(__name__)
aut = Automation()

@app.route('/')
def index():
    thread = Thread(target=aut.run()) 
    thread.start()
    return render_template('index.html')

@app.route('/activate/')
def light_on():
    ls.activate()
    return render_template('index.html')

if __name__ == '__main__':
    ls = LightSwitch()
    app.run(debug=False, host='0.0.0.0')
