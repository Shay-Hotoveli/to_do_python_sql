import pytest
from app.config import get_db_connection

@pytest.fixture(scope="function")
def db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    yield cursor
    conn.rollback()
    cursor.close()
    conn.close()

@pytest.fixture
def clean_user_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM users 
        WHERE user_name LIKE 'testuser_%' 
           OR user_name LIKE 'exist_%' 
           OR user_name LIKE 'newuser_%'
    """)
    conn.commit()
    cur.close()
    conn.close()


