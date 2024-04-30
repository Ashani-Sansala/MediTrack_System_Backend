from config.dbConn import HOST, USER, PASSWORD, DATABASE
import mysql.connector

def get_database_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )