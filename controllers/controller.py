from main import app
from flask import request


@app.route('/', methods=['GET', 'POST'])
def index(data=None):
    if request.method == 'POST':
        data = request.args['sent_data']

        if data is not None:
            return 'POST with param seems to work'
        
        return 'POST(no param) seems to work'

    return 'GET seems to work'

@app.route('/create', methods=['GET', 'POST'])
def create(name=None):
    if request.method == 'POST':
        name = request.form['name']

    return
