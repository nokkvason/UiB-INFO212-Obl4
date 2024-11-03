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
    if category == 'customer':
        return read_customer(data)
    elif category == 'employee':
        return read_employee(data)
    elif category == 'car':
        return read_car(data)
    else:
        return 'None/invalid category for node reading'

def update_node(category, data):
    if category == 'customer':
        return update_customer(data)
    elif category == 'employee':
        return update_employee(data)
    elif category == 'car':
        return update_car(data)
    else:
        return 'None/invalid category for node update'

def delete_node(category, id):
    if category == 'customer':
        return delete_customer(id)
    elif category == 'employee':
        return delete_employee(id)
    elif category == 'car':
        return delete_car(id)
    else:
        return 'None/invalid category for node deletion'


# CRUD functions per category
# Create
def create_customer(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:User {name: $name, age: $age, address: $address, id: $id})', 
                             name=data['name'], age=data['age'], address=data['address'], id=data['id'])

    return 'Creating User node ' + data['name']

def create_employee(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:Employee {name: $name, age: $age, address: $address, branch: $branch, id: $id})', 
                             name=data['name'], age=data['age'], address=data['address'], branch=data['branch'], id=data['id'])
        
    return 'Creating Employee node ' + data['name']

def create_car(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:Car {make: $make, model: $model, year: $year, location: $location, status: $status, id: $id})',
                             make=data['make'], model=data['model'], year=data['year'], location=data['location'], status=data['status'], id=data['id'])
        
    return 'Creating Car node ' + data['id']


#Read
def read_customer(form):
    data = []
    with get_connected() as driver:
        records = driver.execute_query(f'MATCH (u:User {{name: \"{form["name"]}\"}}) RETURN u').records
    
    for record in records:
        data.append(record.data())

    return data

def read_employee(form):
    data = []
    with get_connected() as driver:
        records = driver.execute_query(f'MATCH (e:Employee {{name: \"{form["name"]}\"}}) RETURN e').records

    for record in records:
        data.append(record.data())
    
    return data

def read_car(form):
    data = []
    with get_connected() as driver:
        records = driver.execute_query(f'MATCH (c:Car {{id: \"{form["id"]}\"}}) RETURN c').records

    for record in records:
        data.append(record.data())

    return data
        


#Update
def update_customer(data):
    with get_connected() as driver:
        driver.execute_query(f'''
                             MATCH (u:User {{name: \"{data["name"]}\"}})
                             SET u.{data["property"]} = \"{data["property_value"]}\"
                             ''')
    
    return f'Updating User node {data["name"]}, setting {data["property"]} to {data["property_value"]}'

def update_employee(data):
    with get_connected() as driver:
        driver.execute_query(f'''
                             MATCH (e:Employee {{name: \"{data["name"]}\"}})
                             SET e.{data["property"]} = \"{data["property_value"]}\"
                             ''')
    
    return f'Updating Employee node {data["name"]}, setting {data["property"]} to {data["property_value"]}'

def update_car(data):
    with get_connected() as driver:
        driver.execute_query(f'''
                             MATCH (c:Car {{id: \"{data["id"]}\"}})
                             SET c.{data["property"]} = \"{data["property_value"]}\"
                             ''')
    
    return f'Updating Car node {data["id"]}, setting {data["property"]} to {data["property_value"]}'


#Delete
def delete_customer(form):
    with get_connected() as driver:
        driver.execute_query('MATCH (u:User {name: $name}) DELETE u', name=form['name'])

    return 'Deleting User node ' + form['name']

def delete_employee(form):
    with get_connected() as driver:
        driver.execute_query('MATCH (e:Employee {name: $name}) DELETE e', name=form['name'])

    return 'Deleting Employee node ' + form['name']

def delete_car(form):
    with get_connected() as driver:
        driver.execute_query('MATCH (c:Car {id: $id}) DELETE c', id=form['id'])

    return 'Deleting Car node ' + form['id']
