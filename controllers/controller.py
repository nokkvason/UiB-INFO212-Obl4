from main import app
from flask import request
from models.model import create_node, delete_node


@app.route('/')
def index():
    return 'GET seems to work'



#######################
# Direct CRUD routing #
#######################

@app.route('/crud/')
def noop_crud():
    return '''No CRUD operation selected.\n Please use /crud/<x>, replacing <x> with any one of "c", "r", "u" or "d".'''

@app.route('/crud/<string:crud>', methods=['GET', 'POST'])
def crud(crud):
    crud = str(crud)
    valid = ['c', 'r', 'u', 'd']

    if request.method == 'POST':

        if crud not in valid:
            return '''Invalid CRUD operation selected.\n Please use /crud/<x>, replacing <x> with any one of "c", "r", "u" or "d".'''
        
        if crud == 'c':
            return create_node(request.form['category'], request.form)
        
        elif crud == 'r':
            return 'Reading'
        
        elif crud == 'u':
            return 'Updating'
        
        elif crud == 'd':
            return delete_node(request.form['category'], request.form)

        return 'Something went wrong...'
    return 'GET ' + crud
