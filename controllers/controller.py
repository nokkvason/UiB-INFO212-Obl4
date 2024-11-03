from main import app
from flask import request
from models.model import create_node, read_node, delete_node


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
            return read_node(request.form['category'], request.form)
        
        elif crud == 'u':
            return 'Updating'
        
        elif crud == 'd':
            return delete_node(request.form['category'], request.form)

        return 'POST received but no action taken.'
    return 'GET dunked onnnnnn '


############################
# Rental functions routing #
############################

@app.route('/order-car/<customer_id>/<car_id>')
def order_car():
    pass

@app.route('/cancel-order-car/<customer_id>/<car_id>')
def cancel_order():
    pass

@app.route('/rent-car/<customer_id>/<car_id>')
def rent_car():
    pass

@app.route('/return-car/<customer_id>/<car_id>')
def return_car():
    pass
