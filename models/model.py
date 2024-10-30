from secret import URI, AUTH
from neo4j import GraphDatabase, Driver

def get_connected() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def create_node(category, data):
    if category == 'customer':
        return create_customer(data)

def delete_node(category, id):
    if category == 'customer':
        return delete_customer(id)


def create_customer(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:User {name: $name, age: $age, address: $address})', 
                             name=data['name'], age=data['age'], address=data['address'])

    return 'Creating User node ' + data['name']

def delete_customer(name):
    with get_connected() as driver:
        driver.execute_query('MATCH (u:User {name: $name}) DELETE u', name=name['name'])

    return 'Deleting User node ' + name['name']
