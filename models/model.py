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
        driver.execute_query('CREATE (u:User {name: $name, age: $age, address: $address, id: $id})', 
                             name=data['name'], age=data['age'], address=data['address'], id=data['id'])

    return 'Creating User node ' + data['name']

def create_employee(data):
    with get_connected() as driver:
        driver.execute_query('''
                             MATCH (b:Branch {name: $branch})
                             CREATE (e:Employee {name: $name, age: $age, address: $address, branch: $branch, id: $id})-[:WORKS_AT]->(b)''', 
                             name=data['name'], age=data['age'], address=data['address'], branch=data['branch'], id=data['id'])
        
    return 'Creating Employee node ' + data['name']

def create_car(data):
    with get_connected() as driver:
        driver.execute_query('''
                             MATCH (b:Branch {name: $location})
                             CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status, id: $id})-[:LOCATED_AT]->(b)''',
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
        driver.execute_query('''MATCH (u:User {name: $name}) 
                             OPTIONAL MATCH (u)-[r]->()
                             DELETE u, r''', name=form['name'])

    return 'Deleting User node ' + form['name']

def delete_employee(form):
    with get_connected() as driver:
        driver.execute_query('''MATCH (e:Employee {name: $name})
                             OPTIONAL MATCH (u)-[r]->()
                             DELETE e, r''', name=form['name'])

    return 'Deleting Employee node ' + form['name']

def delete_car(form):
    with get_connected() as driver:
        driver.execute_query('''MATCH (c:Car {id: $id}) 
                             OPTIONAL MATCH (u)-[r]->()
                             DELETE c, r''', id=form['id'])

    return 'Deleting Car node ' + form['id']


#Rental Service functions
def order_car(customer_id, car_id):
    with get_connected() as driver:
        if not has_booked(customer_id=customer_id, car_id=car_id) == 'True':
            driver.execute_query(f"""
                                MATCH (u:User {{id: \"{customer_id}\"}})
                                MATCH (c:Car {{id: \"{car_id}\"}})
                                SET c.status = 'booked'
                                CREATE (u)-[:BOOKED]->(c)
                                """)
        else:
            return f"User {customer_id} has already booked a car"

    return f"User {customer_id} has ordered car {car_id}"

def cancel_order_car(customer_id, car_id):
    with get_connected() as driver:
        if has_booked(customer_id=customer_id, car_id=car_id) == 'True':
            driver.execute_query(f"""
                                MATCH (u:User {{id: \"{customer_id}\"}})
                                MATCH (c:Car {{id: \"{car_id}\"}})
                                MATCH (u)-[r:BOOKED]->(c)
                                SET c.status = "available"
                                DELETE r
                                """)
        else:
            return f"User {customer_id} has not booked this car"

    return f"User {customer_id} has canceled booking for car {car_id}"

def rent_car(customer_id, car_id):
    with get_connected() as driver:
        if has_booked(customer_id=customer_id, car_id=car_id) == 'True':
            driver.execute_query(f"""
                                MATCH (u:User {{id: \"{customer_id}\"}})
                                MATCH (c:Car {{id: \"{car_id}\"}})
                                MATCH (u)-[r:BOOKED]->(c)
                                SET c.status = "rented"
                                DELETE r
                                CREATE (u)-[:RENTED]->(c)
                                """)
        else:
            return f"User {customer_id} has not booked this car"
        
    return f"User {customer_id} has rented car {car_id}"

def return_car(customer_id, car_id, car_status):
    with get_connected() as driver:
        if has_rented(customer_id=customer_id, car_id=car_id) == 'True':
            driver.execute_query(f"""
                                 MATCH (u:User {{id: \'{customer_id}\'}})
                                 MATCH (c:Car {{id: \'{car_id}\'}})
                                 MATCH (u)-[r:RENTED]->(c)
                                 SET c.status = "{car_status}"
                                 DELETE r
                                 """)
        else:
            return f"User {customer_id} has not rented car {car_id}"
    
    return f"User {customer_id} has returned car {car_id}"


#Intermediate functions
def has_booked(customer_id, car_id):
    with get_connected() as driver:
        result = driver.execute_query(f"""
                                    MATCH (u:User {{id: \'{customer_id}\'}})
                                    MATCH (c:Car {{id: \'{car_id}\'}})
                                    RETURN EXISTS {{(u)-[BOOKED]->(c)}}
                                    """).records
    return str(result[0][0])

def has_rented(customer_id, car_id):
    with get_connected() as driver:
        result = driver.execute_query(f"""
                                      MATCH (u:User {{id: \'{customer_id}\'}})
                                      MATCH (c:Car {{id: \'{car_id}\'}})
                                      RETURN EXISTS {{(u)-[RENTED]->(c)}}
                                      """).records
    return str(result[0][0])
