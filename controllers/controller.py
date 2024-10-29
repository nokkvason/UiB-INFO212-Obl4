from main import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html')
