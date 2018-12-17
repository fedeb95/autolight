from flask import Flask, render_template,request,redirect,url_for
from autolight import Autolight
from threading import Thread
import logging

al=Autolight()
app = Flask(__name__)
al.start()
Thread(target=al.run)
print("ok")

@app.route('/')
def index():
    if al.ls.is_on():
        return render_template('index.html', image="/static/on.png", override=al.override)
    else:
        return render_template('index.html', image="/static/off.png", override=al.override)

@app.route('/activate/')
def light_on():
    al.light_switch_mylock.acquire()
    al.ls.activate()
    al.light_switch_mylock.release()
    return redirect(url_for('index'))

@app.route('/override/')
def over():
    al.override = al.override ^ True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
