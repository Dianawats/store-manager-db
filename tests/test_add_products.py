from tests.base_test import BaseTestCase
from run import app
from flask import jsonify, json

class TestProducts(BaseTestCase):

    def test_add_product_successfully(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             ) 
        reply = json.loads(response.data.decode())
        self.assertIn(("Rice"), reply.get("New Product").values())
        self.assertEqual(response.status_code, 201)

    def test_add_product_exists_product(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )                      
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "The product inserted already exists, add a new product")
        self.assertEqual(response.status_code, 200)
    
    def test_add_product_no_price(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity=" ",price=" "),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "quantity should only be digits with no white spaces")
        self.assertEqual(response.status_code, 400)

    def test_add_product_no_product_2(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product=" ", quantity="20",price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "product name is missing")
        self.assertEqual(response.status_code, 400)

    def test_add_product_success(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20", price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertTrue(reply.get)
        self.assertEqual(response.status_code, 201)

    def test_add_product_wrong_quantity(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertTrue(reply.get)
        self.assertEqual(response.status_code, 201)

    def test_add_product_with_add_authorization(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertTrue(reply.get)
        self.assertEqual(response.status_code, 201)

    def test_add_product_zero_quantity(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertTrue(reply.get)
        self.assertEqual(response.status_code, 201)        

    def test_add_product_wrong_price(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="yz"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "price should only be digits with no white spaces")
        self.assertEqual(response.status_code, 400)

    def test_add_product_zero_price(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="0"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "price should be greater than zero or more")
        self.assertEqual(response.status_code, 400)    

    def test_add_product_short_product(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Ri", quantity="20",price="4000"),)   
                             )          
        reply = json.loads(response.data.decode())
        self.assertEqual(reply.get("message"), "product name should be more than 3 characters long")
        self.assertEqual(response.status_code, 400)
        
                        