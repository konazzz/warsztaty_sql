from psycopg2 import connect, OperationalError, DuplicateDataBase, DuplicateTable
USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"



def create_db():
    sql = """
    CREATE DATABASE my_app"""
    cnx = connect(user=USER, host=HOST, password=PASSWORD)
    cursor = cnx.cursor()
    try:
        cursor.execute(sql)
    except (DuplicateDataBase, OperationalError):
        return "the database already exists"
    cnx.close()
    return "success"



def create_user_table():
    sql = """
    CREATE TABLE user
    (id SERIAL PRIMARY KEY
    username VARCHAR(255)
    hashed_password VARCHAR(80))
    """
    cnx = connect(user=USER, host=HOST, password=PASSWORD, database="my_app")
    cursor = cnx.cursor()
    try:
        cursor.execute(sql)
    except (DuplicateTable, OperationalError):
        return "the table already exists"
    cnx.close()
    return "success"

def create_msg_table():
    sql = """
    id SERIAL PRIMARY KEY
    from_id INT FOREIGN KEY REFERENCES user (id)
    to_id INT FOREIGN KEY REFERENCES user (id)
    creation_date TIMESTAMP
    'text' text varchar(255)
    """
    cnx = connect(user=USER, host=HOST, password=PASSWORD, database="my_app")
    cursor = cnx.cursor()
    try:
        cursor.execute(sql)
    except (DuplicateTable, OperationalError):
        return "the table already exists"
    cnx.close()
    return "success"