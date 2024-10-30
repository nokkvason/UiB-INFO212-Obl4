from main import app
from flask import request


@app.route('/')
def index():
    return

@app.route('/create', methods=['GET', 'POST'])
def create(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return
