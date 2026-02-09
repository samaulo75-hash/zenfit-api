import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="almohada11",
        database="zenfit",
        auth_plugin="mysql_native_password"
    )
