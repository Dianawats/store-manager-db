from app.db.databasemanager import DatabaseConnection 

class DBMethods:
    def __init__(self):
        self.connect = DatabaseConnection()
        self.cursor = self.connect.dict_cursor

    def add_new_user(self, username, phone, role, password):
        """This method registers a user"""
        query = (
            """INSERT INTO users (username, phone, role, password) 
               VALUES ('{}', '{}', '{}', '{}')""".format(username, phone, role, password))
        self.cursor.execute(query)

    def does_username_exist(self,username):
        """
        This method checks whether there's an existing username
        """
        query = ("""SELECT * FROM users where username = '{}'""".format(username))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        if user:
            return user
        return False    

    def does_phone_exist(self,phone):
        """
        This method checks whether there's an existing phone
        """
        query = ("""SELECT * FROM users where phone = '{}'""".format(phone))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        if user:
            return True
        return False        

    def user_login(self, username, password):
        """This method checks for user login"""
        query = ("""SELECT * from users where username = '{}' and password='{}'""".format(username, password))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        return user