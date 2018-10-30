from flask import jsonify, request, Blueprint
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.validation import Validator
from app.handlers.product_handler import ProductHandler

validate = Validator()
product_handler = ProductHandler()
views_blueprint = Blueprint("views_blueprint", __name__)


class AddProduct(MethodView):
    """This class adds products"""
    def post(self):
        try:
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
                product_exists = product_handler.does_product_exist(
                    product_name=product)
                if product_exists:
                    new_quantity = product_exists["quantity"] + int(quantity)
                    product_handler.update_product(product_name=product,
                                                      quantity=new_quantity,
                                                      price=price, 
                                                      product_id=product_exists["product_id"])
                    return jsonify({
                        "message":
                            "product already exists, its quantity has been updated", "Updated Product":
                            product_handler.get_single_product(product_exists["product_id"])}), 200
                product_added = product_handler.add_product(product_name=product, quantity=int(
                    quantity), price=int(price))
                if product_added:
                    return jsonify({
                        "message":
                        "product added successfully.", "New Product": product_handler.does_product_exist(product_name=product)
                    }), 201
                return jsonify({"message": "product not yet added"}), 400
            return jsonify({"message": "You missed some key in your request body"}), 400
        except Exception as exception:
            return jsonify({"message": str(exception)}), 400

add_product_view = AddProduct.as_view("add_product_view")
views_blueprint.add_url_rule("/api/v1/products", view_func=add_product_view, methods=["POST"])


