from main import app
from flask import render_template, request


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return render_template('create.html', name = name)
