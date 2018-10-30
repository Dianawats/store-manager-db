import psycopg2
import psycopg2.extras as extra
from app import app

class DatabaseConnection:
    """
    This class does all database related stuff
    """

    def __init__(self):
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
                phone VARCHAR(50) NOT NULL,
                role VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
            """,

            """
			CREATE TABLE IF NOT EXISTS products (
				product_id SERIAL PRIMARY KEY,
					product VARCHAR(255) NOT NULL,
					quantity INTEGER NOT NULL,
					price INTEGER NOT NULL,
                    reg_date timestamp NOT NULL
							
						)
					"""
        )
           
        for query in queries:
            self.dict_cursor.execute(query)

    def delete_test_tables(self):

        delete_queries = (
            """DROP TABLE IF EXISTS users CASCADE""",

            """DROP TABLE IF EXISTS products CASCADE""",

        )
        for query in delete_queries:
            self.dict_cursor.execute(query)