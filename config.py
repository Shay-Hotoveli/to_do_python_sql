from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

secret_key = os.getenv('SECURE_KEY')

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection