from flask import Flask, render_template,request
from light_switch import LightSwitch
from threading import Thread


app = Flask(__name__)
ls = LightSwitch(pin=2,on=False)

@app.route('/')
def index():
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")

@app.route('/activate/')
def light_on():
    ls.activate()
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
