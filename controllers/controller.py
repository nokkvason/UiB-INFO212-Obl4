from main import app
from flask import render_template, request


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emplog/', methods=['GET', 'POST'])
def emplog(logged_in=False):
    if request.method == 'POST':
        logged_in = True

    return render_template('employeelogin.html', emp=logged_in)


################
# CRUD routing #
################

@app.route('/create/', methods=['GET', 'POST'])
def create(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return render_template('create.html', name = name)

@app.route('/read/', methods=['GET', 'POST'])
def read(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return render_template('read.html', name = name)

@app.route('/update/', methods=['GET', 'POST'])
def update(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return render_template('update.html', name = name)

@app.route('/delete/', methods=['GET', 'POST'])
def delete(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return render_template('delete.html', name = name)
