from main import app
from flask import request
from models.model import create_node, read_node, update_node, delete_node, order_car, has_booked


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
            return update_node(request.form['category'], request.form)
        
        elif crud == 'd':
            return delete_node(request.form['category'], request.form)

        return 'POST received but no action taken.'
    return 'GET dunked onnnnnn '


############################
# Rental functions routing #
############################

@app.route('/order-car/<customer_id>/<car_id>')
def ROUTE_order_car(customer_id, car_id):
    return order_car(customer_id=customer_id, car_id=car_id)

@app.route('/cancel-order-car/<customer_id>/<car_id>')
def ROUTE_cancel_order():
    pass

@app.route('/rent-car/<customer_id>/<car_id>')
def ROUTE_rent_car():
    pass

@app.route('/return-car/<customer_id>/<car_id>')
def ROUTE_return_car():
    pass


#Testing
@app.route('/test-if-booked/<customer_id>')
def test_booking(customer_id):
    return has_booked(customer_id=customer_id)
