import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables to set database connection details
HOST = os.getenv('HOST')         # Retrieve database host
USER = os.getenv('USER')         # Retrieve database username
PASSWORD = os.getenv('PASSWORD') # Retrieve database password
DATABASE = os.getenv('DATABASE') # Retrieve database name

# Validate database connection details
if not (HOST and USER and PASSWORD and DATABASE):
    raise ValueError("Database information error!")

def get_database_connection():
    
    # Establishes a connection to the MySQL database using environment variables.
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
