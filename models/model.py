from secret import URI, AUTH
from neo4j import GraphDatabase, Driver

def get_connected() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

# Top level CRUD functions
def create_node(category, data):
    if category == 'customer':
        return create_customer(data)
    elif category == 'employee':
        return create_employee(data)
    elif category == 'car':
        return create_car(data)
    else:
        return 'None/invalid category for node creation'

def read_node(category, data):
    pass

def update_node(category, data):
    pass

def delete_node(category, id):
    if category == 'customer':
        return delete_customer(id)
    if category == 'employee':
        return delete_employee(id)
    if category == 'car':
        return delete_car(id)


# CRUD functions per category
# Create
def create_customer(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:User {name: $name, age: $age, address: $address})', 
                             name=data['name'], age=data['age'], address=data['address'])

    return 'Creating User node ' + data['name']

def create_employee(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:Employee {name: $name, age: $age, address: $address, branch: $branch})', 
                             name=data['name'], age=data['age'], address=data['address'], branch=data['branch'])
        
    return 'Creating Employee node ' + data['name']

def create_car(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:Car {make: $make, model: $model, year: $year, location: $location, status: $status, id: $id})',
                             make=data['make'], model=data['model'], year=data['year'], location=data['location'], status=data['status'], id=data['id'])
        
    return 'Creating Car node ' + data['id']


#Read


#Update


#Delete
def delete_customer(name):
    with get_connected() as driver:
        driver.execute_query('MATCH (u:User {name: $name}) DELETE u', name=name['name'])

    return 'Deleting User node ' + name['name']

def delete_employee(name):
    with get_connected() as driver:
        driver.execute_query('MATCH (e:Employee {name: $name}) DELETE e', name=name['name'])

    return 'Deleting Employee node ' + name['name']

def delete_car(id):
    with get_connected() as driver:
        driver.execute_query('MATCH (c:Car {id: $id}) DELETE c', id=id['id'])

    return 'Deleting Car node ' + id['id']
