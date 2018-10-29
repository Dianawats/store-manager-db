from app import app
from flask import request, jsonify
from .models.product import Product
from .models.sales import SaleRecord
from app.validation import Validator


"""
Product Views to handle requests with products endpoints
"""
@app.route("/api/v1/products",methods=["POST"])
#This defines our route as being /api/v1/products 
# & as being accessible only via a get request
def add_product():
    #assign the method to it to return the string
    data = request.get_json()
    search_keys = ("product", "quantity", "price")
    if all(key in data.keys() for key in search_keys):
        product = data.get("product")
        quantity = data.get("quantity")
        price = data.get("price")

        invalid = validation_obj.validate_product_inputs(product, quantity, price)
        if invalid:
            return jsonify({"message":invalid}), 400
        if any(prodct["product"] == product for prodct in product_obj.all_products):
            return jsonify({"message":
                            "The product inserted already exists, add a new product"}), 409
        if (product_obj.add_product(product, quantity, price)):
            return jsonify({"message":"product added successfully", 
                            "products":product_obj.all_products}), 201
    return jsonify({"message": "You missed some key in your request body"}), 400 

@app.route("/api/v1/products", methods=["GET"])
#get all products
def get_all_products():
    all_products = product_obj.get_all_products()
    if all_products:
        return jsonify({"All Products":all_products}), 200
    return jsonify({"message":"products not yet added"}), 404 

@app.route("/api/v1/products/<product_id>", methods=["GET"])
#get a single product
def get_single_product(product_id):
    invalid = validation_obj.validate_input_type(product_id)
    if invalid:
        return jsonify({"message":invalid}), 400
    single_product = product_obj.get_single_product(product_id)
    if single_product:
        return jsonify({"product details": single_product}), 200
    return jsonify({"message":"product not yet added"}), 404

"""
Sales View to handle requests with sales endpoint
"""
@app.route("/api/v1/sales", methods=["POST"])
#adding sales record
def create_sales_record():
    # extract request data
    data = request.get_json()
    search_keys = ( "product","quantity", "amount")
    if all(key in data.keys() for key in search_keys):
        product = data.get("product")
        quantity = data.get("quantity")
        amount = data.get("amount")

        invalid_values = validation_obj.validate_product_inputs(product, quantity, amount)
        if invalid_values:
            return jsonify({"message":invalid_values}), 400
        if (sale_obj.create_sale_record(product, quantity, amount)):
            return jsonify({"message":"Sale record successfully created", 
                            "Sales":sale_obj.all_Sales}), 201
        else:
            return jsonify({"message":"No sale record created yet"}), 400
    else:
        return jsonify({"message": 
                        "You missed some key in your request body"}), 400

@app.route("/api/v1/sales", methods=["GET"])
# view all sales
def get_all_sales():
    all_sales = sale_obj.get_all_sales()
    if all_sales:
        return jsonify({"All Sales":sale_obj.all_Sales}), 200
    return jsonify({"message":"no sales created yet"}), 404 

@app.route("/api/v1/sales/<sale_id>", methods=["GET"])
# getting a single sale record
def get_single_sale(sale_id):
    invalid = validation_obj.validate_input_type(sale_id)
    if invalid:
        return jsonify({"message":invalid}), 400
    single_sale = sale_obj.get_single_sale(sale_id)
    if single_sale:
        return jsonify({"sale details": single_sale}), 200
    return jsonify({"message":"sale not created yet"}), 404

product_obj = Product()
sale_obj = SaleRecord()
validation_obj = Validator()
