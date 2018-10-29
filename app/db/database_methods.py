from app.db.databmanager import DatabaseConnection 

class DBFunctions:
    def __init__(self):
        self.connect = DatabaseConnection()
        self.cursor = self.connect.dict_cursor

    def add_new_user(self, username, contact, role, password):
        """This method registers a user"""
        query = (
            """INSERT INTO users (username, contact, role, password) 
               VALUES ('{}', '{}', '{}', '{}')""".format(username, contact, role, password))
        self.cursor.execute(query)