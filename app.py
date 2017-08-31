from flask import Flask, render_template,request
from prova import Automation
from threading import Thread

app = Flask(__name__)
aut = Automation()
thread = Thread(target=aut.run())
thread.start()

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
