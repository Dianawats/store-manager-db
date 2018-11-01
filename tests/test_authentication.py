from tests.base_test import BaseTestCase
from run import app
from flask import jsonify, json

class Test_authentication(BaseTestCase):

    def test_registration_successfully(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="diana", phone="0700-687656", role="attendant", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "Attendant account has been created")
        self.assertEqual(response.status_code, 201)

    def test_registration_with_short_username(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="di", phone="0700-687656", role="attendant", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "username should be more than 3 characters long")
        self.assertEqual(response.status_code, 400)    

    def test_registration_with_missing_keys(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict( phone="0700-687656", role="attendant", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "You missed some key in your registration body")
        self.assertEqual(response.status_code, 400)    

    def test_registration_with_wrong_username(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="", phone="0700-687656", role="attendant", password="watson"),)
                                 )                       
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "username is missing")
        self.assertEqual(response.status_code, 400)

    def test_registration_with_no_username(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username=" ", phone="0700-687656", role="attendant", password="watson"),)
                                 )                       
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "username should contain no white spaces")
        self.assertEqual(response.status_code, 400)     
    
    def test_registration_with_existing_username(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700-687656", role="attendant", password="watson"),)
                                 )
        response2 = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700-687656", role="attendant", password="watson"),)
                                 )                         
        reply = json.loads(response2.data)
        self.assertEqual(reply.get("message"), "username exists")
        self.assertEqual(response2.status_code, 409)

    def test_registration_with_existing_phone(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="diana", phone="0700-687656", role="attendant", password="watson"),)
                                 )
        response2 = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700-687656", role="attendant", password="watso"),)
                                 )                         
        reply = json.loads(response2.data)
        self.assertEqual(reply.get("message"), "phone exists")
        self.assertEqual(response2.status_code, 409)    

    def test_registration_with_wrong_contact(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700687656", role="attendant", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "phone format should be [07zz-zzzzzz],in digits without white spaces")
        self.assertEqual(response.status_code, 400)

    def test_registration_with_wrong_role(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700-687656", role="attendat", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "role should either be admin or attendant")
        self.assertEqual(response.status_code, 400)

    def test_registration_with_impromper_username(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="  dian", phone="0700-687656", role="attendant", password="watson"),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "username should contain no white spaces")
        self.assertEqual(response.status_code, 400)

    def test_registration_with_no_password(self):
        """ Test for successful user register """
        admin_login= self.admin_login()
        response = self.app.post("/api/auth/register",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(username="dian", phone="0700-687656", role="attendant", password=""),)
                                 )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "password is missing")
        self.assertEqual(response.status_code, 400)            

    def test_user_login_successfully(self):
        """ Test for successful login """
        self.register_attendant()
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username="dian", password="watson"))
        )
        self.assertEqual(response.status_code, 404)

    def test_user_login_not_successful(self):
        """ Test for successful login """
        self.register_attendant()
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username="dian", password="watso"))
        )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "user does not exist")
        self.assertEqual(response.status_code, 404)
    
    def test_user_login_with_wrong_username(self):
        """ Test for successful login """
        self.register_attendant()
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username=" dian", password="dian"))
        )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "user does not exist")
        self.assertEqual(response.status_code, 404)

    def test_user_login_with_no_password(self):
        """ Test for successful login """
        self.register_attendant()
        response = self.app.post(
            "/api/auth/login",
            content_type='application/json',
            data=json.dumps(dict(username="dian", password=""))
        )
        reply = json.loads(response.data)
        self.assertEqual(reply.get("message"), "password is missing")
        self.assertEqual(response.status_code, 400)                     