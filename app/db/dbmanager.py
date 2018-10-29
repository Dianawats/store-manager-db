import pyscopg2
import psycopg2.extras as extra
from app import app

class DatabaseConnection:
    """
    This class does all database related stuff
    """

    def __init__(self):
    """
    Initiates a database connection
    """
        self.conn = psycopg2.connect(
            database="storemanager", 
            user="postgres", 
            password="keko", 
            host="localhost", 
            port="5432")
        self.conn.autocommit = True
        self.dict_cursor = self.conn.cursor(cursor_factory=extra.RealDictCursor)

    def create_tables(self):
        queries = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                contact VARCHAR(50) NOT NULL,
                role VARCHAR(25) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
            """