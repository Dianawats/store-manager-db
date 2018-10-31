from flask import jsonify, request, Blueprint
from flask.views import MethodView
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.validation import Validator
from app.handlers.product_handler import ProductHandler
from app.authentication.authenticate import requires_admin_permission

validate = Validator()
product_handler = ProductHandler()
views_blueprint = Blueprint("views_blueprint", __name__)


class AddProduct(MethodView):

    """This class adds products"""
    # @requires_admin_permission
    def post(self):
        try:
            data = request.get_json()
            search_keys = ("product", "quantity", "price")
            if all(key in data.keys() for key in search_keys):
                product = data.get("product")
                quantity = data.get("quantity")
                price = data.get("price")
                reg_date = datetime.now()

                invalid = validate.product_validator(
                    product, quantity, price)
                if invalid:
                    return jsonify({"message": invalid}), 400
                product_exists = product_handler.does_product_exist(
                    product_name=product)
                if product_exists:
                    new_quantity = product_exists["quantity"] + int(quantity)
                    product_handler.update_product(product_name=product,
                                                      quantity=new_quantity,
                                                      price=price, 
                                                      
                                                      product_id=product_exists["product_id"], reg_date=reg_date)
                                                      
                    return jsonify({
                        "message":
                            "The product inserted already exists, add a new product", "Updated Product":
                            product_handler.get_single_product(product_exists["product_id"])}), 200
                product_added = product_handler.add_product(product_name=product, quantity=int(
                    quantity), price=int(price), reg_date=reg_date)
                if product_added:
                    return jsonify({
                        "message":
                        "product added successfully.", 
                        "New Product": product_handler.does_product_exist(product_name=product)
                    }), 201
                return jsonify({"message": "product not yet added"}), 400
            return jsonify({"message": "You missed some key in your request body"}), 400
        except Exception as exception:
            return jsonify({"message": str(exception)}), 400

class GetAllProducts(MethodView):
    """This class returns all the products added"""

    def get(self):
        all_products = product_handler.get_all_products()
        if all_products:
            return jsonify({"all products": all_products}), 200
        return jsonify({"message": "products not yet added"}), 404

class GetSingleProduct(MethodView):
    """This class gets a particular product"""

    def get(self, product_id):
        invalid = validate.validate_input_type(product_id)
        if invalid:
            return jsonify({"message": invalid}), 400
        product_details = product_handler.get_single_product(
            product_id=product_id)
        if product_details:
            return jsonify({"product details": product_details}), 200
        return jsonify({"message": "no product added yet"}), 404

class UpdateProduct(MethodView):
    """This class updates the product"""

    def put(self, product_id):
        invalid_id = validate.validate_input_type(product_id)
        if invalid_id:
            return jsonify({"message": invalid_id}), 400
        data = request.get_json()
        search_keys = ("product", "quantity", "price")
        if all(key in data.keys() for key in search_keys):
            product = data.get("product")
            quantity = data.get("quantity")
            price = data.get("price")

            invalid = validate.product_validator(
                product, quantity, price)
            if invalid:
                return jsonify({"message": invalid}), 400
            update = product_handler.update_product(
                product_name=product, quantity=quantity, 
                                      price=price,
                                      reg_date=reg_date, 
                                      product_id=product_id)
            if update:
                return jsonify({
                    "message":
                        "product updated successfully.", 
                        "Updated Product": product_handler.get_single_product(product_id=product_id)
                }), 200
            return jsonify({"message": "product not updated or doesn't exist"}), 400
        return jsonify({"message": "You missed some key in your request body"}), 400


# class DeleteProduct(MethodView):
#     """This class deletes the product"""
    
#     def delete(self, product_id):
#         invalid = validate.validate_input_type(product_id)
#         if invalid:
#             return jsonify({"message": invalid}), 400
#         delete = product_handler.delete_product(product_id=product_id)
#         if delete:
#             return jsonify({"message": "product successfully deleted"}), 200
#         else:
#             return jsonify({"message": 
#                             "product not yet deleted, or no existing product"}), 400


add_product_view = AddProduct.as_view("add_product_view")
views_blueprint.add_url_rule(
    "/api/v2/products", view_func=add_product_view, methods=["POST"])

get_all_products_view = GetAllProducts.as_view("get_all_products_view")
views_blueprint.add_url_rule(
    "/api/v2/products", view_func=get_all_products_view, methods=["GET"])

get_single_product_view = GetSingleProduct.as_view("get_single_product_view")
views_blueprint.add_url_rule(
    "/api/v2/products/<product_id>",
                             view_func=get_single_product_view, methods=["GET"]) 

update_product_view = UpdateProduct.as_view("update_product_view")                             
views_blueprint.add_url_rule(
    "/api/v2/products/<product_id>", view_func=update_product_view, methods=["PUT"])

delete_product_view = DeleteProduct.as_view("delete_product_view")
views_blueprint.add_url_rule(
    "/api/v2/products/<product_id>", view_func=delete_product_view, methods=["DELETE"])

