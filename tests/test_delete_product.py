from tests.base_test import BaseTestCase
from run import app
from flask import jsonify, json

class TestDeleteProducts(BaseTestCase):

    def test_delete_no_existing_product(self):
        admin_login= self.admin_login()
        response2 = self.app.delete("/api/v2/products/4",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),)
        reply = json.loads(response2.data.decode())
        self.assertEqual(reply.get("message"), "product not yet deleted, or no existing product")                
        self.assertEqual(response2.status_code, 400)
    
    def test_delete_product(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",unit_price="4000"),)   
                             )
        response2 = self.app.delete("/api/v2/products/1",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),)
        reply = json.loads(response2.data.decode())
        self.assertEqual(reply.get("message"), "product not yet deleted, or no existing product")                
        self.assertEqual(response2.status_code, 400)

    def test_delete_product_with_wrong_id(self):
        admin_login= self.admin_login()
        response = self.app.post("/api/v2/products",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),
                                 data=json.dumps(dict(product="Rice", quantity="20",price="4000"),)   
                             )
        response2 = self.app.delete("/api/v2/products/e",
                                 content_type='application/json', headers=dict(Authorization='Bearer '+admin_login['token']),)                 
        reply = json.loads(response2.data.decode())
        self.assertEqual(reply.get("message"), "Input should be an integer") 
        self.assertEqual(response2.status_code, 400)    