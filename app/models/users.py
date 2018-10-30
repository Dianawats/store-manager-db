class User:
    "This a user class model"
    
    def __init__(self, user_name, contact, role, password):
        self.user_name = user_name
        self.contact = contact
        self.role = role
        self.password = password
    