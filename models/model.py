from secret import URI, AUTH
from neo4j import GraphDatabase, Driver

def get_connected() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def create_new_customer(data):
    with get_connected() as driver:
        driver.execute_query('CREATE (a:User {name: $name, age: $age, address: $address})', 
                             name=data['name'], age=data['age'], address=data['address'])

    # result = f'CREATE (a:User {{name:{data['name']}, age:{data['age']}, address:{data['address']}}})'

    return 'Creating User node ' + data['name']
