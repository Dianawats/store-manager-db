import unittest
from run import app
from flask import json
from app.db.databmanager import DatabaseConnection
from app.handlers.user_handler import UserHandler

connection = DatabaseConnection()
user_handler = UserHandler()

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.username = "beutrice"
        self.phone = "0700-607656"
        self.role = "admin"
        self.password = "watson"
        self.app = app.test_client(self)
        connection.create_tables()
        self.register_admin()
        self.register_attendant()
        
    def tearDown(self):
        """This method drops tables after the test is run"""
        connection.delete_test_tables()

    def register_admin(self):
        user_handler.add_attendant(self.username, self.phone, self.role, self.password)
        
    def register_attendant(self):
        user_handler.add_attendant("carol", "0700-600658", "attendant", "diate")
    
    def admin_login(self):
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username=self.username, password=self.password))
        )
        reply = json.loads(response.data)
        return reply
    
    def attendant_login(self):
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username="dian", password="watson"))
        )
        reply = json.loads(response.data)
        return reply    