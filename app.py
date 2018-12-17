from flask import Flask, render_template,request,redirect,url_for

al=Autolight()
app = Flask(__name__)

@app.route('/')
def index():
    if ls.is_on():
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
    al.override = al.verride ^ True
    return redirect(url_for('index'))


if __name__ == '__main__':
    # get config, if train=True don't start nn in a new thread but enable training, otherwise only new thread without training
    al.run()
    app.run(debug=True, host='0.0.0.0')
