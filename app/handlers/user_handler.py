from app.db.database_methods import DBMethods
from app.models.user import User


class UserHandler:
    """This class handles user"""

    def __init__(self):
        self.dbconn = DBMethods()

    def add_attendant(self, username, phone, role, password):
        """This method adds new attendant"""

        user = User(username, phone, role, password)
        self.dbconn.add_new_user(
            username=user.username, phone=user.phone, 
                                    role=user.role, 
                                    password=user.password)
        return True
    
    def check_whether_user_exists(self, username):
        """
        This method checks wether the user supplied exists already
        """
        exists_user = self.dbconn.does_username_exist(username=username)
        if exists_user:
            return True
        return False

    def check_whether_phone_exist(self, phone):
        """
        This method checks whether the phone supplied already exists
        """
        phone_exists = self.dbconn.does_phone_exist(phone=phone)
        if phone_exists:
            return True
        return False

    def user_login(self, username, password):
        """This method checks for user login"""
        login = self.dbconn.user_login(username=username, password=password)
        if login:
            return login
        return False

    def get_user_role(self, username):
        """This method gets the current user role"""
        user = self.dbconn.does_username_exist(username=username)
        return user    
