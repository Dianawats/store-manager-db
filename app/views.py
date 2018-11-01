from flask import jsonify, request, Blueprint
from flask.views import MethodView
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.validation import Validator
from app.db.database_methods import DBMethods
from app.handlers.product_handler import ProductHandler
from app.handlers.sale_handler import SaleHandler
from app.handlers.user_handler import UserHandler
from app.authentication.authenticate import requires_admin_permission

validate = Validator()
user_handler = UserHandler()
sale_handler = SaleHandler()
db_meth = DBMethods()
product_handler = ProductHandler()
views_blueprint = Blueprint("views_blueprint", __name__)


class AddProduct(MethodView):
    @requires_admin_permission
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
                            "The product inserted already exists, add a new product", "Updated Product":
                            product_handler.get_single_product(product_exists["product_id"])}), 200
                product_added = product_handler.add_product(product_name=product, quantity=int(
                    quantity), price=int(price))
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
    @jwt_required
    def get(self):
        all_products = product_handler.get_all_products()
        if all_products:
            return jsonify({"all products": all_products}), 200
        return jsonify({"message": "products not yet added"}), 404

class GetSingleProduct(MethodView):
    @jwt_required
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
    @requires_admin_permission
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
                product_name=product, quantity=quantity, price=price, product_id=product_id)
            if update:
                return jsonify({
                    "message":
                        "product updated successfully.", "Updated Product": product_handler.get_single_product(product_id=product_id)
                }), 200
            return jsonify({"message": "product not updated or doesn't exist"}), 400
        return jsonify({"message": "You missed some key in your request body"}), 400

class DeleteProduct(MethodView):
    @jwt_required
    def delete(self, product_id):
        invalid = validate.validate_input_type(product_id)
        if invalid:
            return jsonify({"message": invalid}), 400
        delete = product_handler.delete_product(product_id=product_id)
        if delete:
            return jsonify({"message": "product successfully deleted"}), 200
        else:
            return jsonify({"message": 
                            "product not yet deleted, or no existing product"}), 400


class CreateSalesRecord(MethodView):
    @jwt_required
    def post(self, product_id):
        data = request.get_json()
        if "quantity" in data.keys():
            quantity = data.get("quantity")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendant = get_jwt_identity()
            invalid_quantity = validate.validate_input_type(quantity)
            if invalid_quantity:
                return jsonify({"message": invalid_quantity}), 400
            invalid_id = validate.validate_input_type(product_id)
            if invalid_id:
                return jsonify({"message": invalid_id}), 400
            make_sale = sale_handler.add_sale_record(
                product_id=product_id, quantity=quantity, attendant=attendant, date=date)
            if make_sale:
                return jsonify({"message": "sale record added successfully", "sales": db_meth.get_new_sale()}), 201
            else:
                return jsonify({"message": "sale record is not added or product is not available"}), 400

class GetSingleSaleRecord(MethodView):
    @jwt_required
    def get(self, sale_id):
        invalid = validate.validate_input_type(sale_id)
        if invalid:
            return jsonify({"message": invalid}), 400
        logged_user = get_jwt_identity()
        user_role = user_handler.get_user_role(username=logged_user)
        if user_role["role"] == 'admin':    
            sale_record = sale_handler.get_single_sale(sale_id=sale_id)
        elif user_role["role"] == 'attendant':
            sale_record = sale_handler.get_single_sale_for_user(sale_id=sale_id, username=logged_user)
        if sale_record:
            return jsonify({"Sale details": sale_record}), 200
        return jsonify({"message": "sale record not yet added"}), 404

class GetAllSales(MethodView):
    @jwt_required
    def get(self):
        logged_user = get_jwt_identity()
        user_role = user_handler.get_user_role(username=logged_user)
        if user_role["role"] == 'admin':
            all_sales = sale_handler.get_all_sales()
        elif user_role["role"] == 'attendant':
            all_sales = sale_handler.get_all_sales_for_user(username=logged_user)
        if all_sales:
            return jsonify({"Sale Records": all_sales}), 200
        return jsonify({"message": "no sles recorded yet"}), 404     


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

single_sales_view = GetSingleSaleRecord.as_view("single_sales_view")
views_blueprint.add_url_rule("/api/v2/sales/<sale_id>", view_func=single_sales_view, methods=["GET"])

make_sales_view = CreateSalesRecord.as_view("make_sales_view")
views_blueprint.add_url_rule("/api/v2/sales/<product_id>", view_func=make_sales_view, methods=["POST"])

all_sales_view = GetAllSales.as_view("all_sales_view")
views_blueprint.add_url_rule("/api/v2/sales", view_func=all_sales_view, methods=["GET"])

