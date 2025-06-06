import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECURE_KEY", "fallback_key")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
