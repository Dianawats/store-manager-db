from app.models.product import Product
from app.db.database_methods import DBMethods


class ProductHandler:
    """This class handles products"""
    def __init__(self):
        self.dbconn = DBMethods()

    def add_product(self, product_name, quantity, price, reg_date):
        """This method creates a new product"""
        new_product = Product(product_name=product_name,
                              quantity=quantity, price=price, reg_date=reg_date)
        self.dbconn.add_new_product(product=new_product.product_name,
                                   quantity=new_product.quantity, 
                                   price=new_product.price, reg_date=reg_date)
        return True

    def does_product_exist(self, product_name):
        """This method checks if product exists"""
        product_exists = self.dbconn.does_product_exist(product=product_name)
        if product_exists:
            return product_exists
        return False

    def update_product(self, product_name, quantity, price, product_id, reg_date):
        """This method updates a product"""
        update = self.dbconn.update_product(
            product=product_name, quantity=quantity, price=price, product_id=product_id,  reg_date=reg_date)
        if update:
            return True
        else:
            return False

    def get_single_product(self, product_id):
        """This method adds a single product"""
        product = self.dbconn.get_single_product(product_id=product_id)
        if product:
            return product
        return False

    def get_all_products(self):
        """This method gets all available products"""
        all_products = self.dbconn.get_all_products()
        return all_products

    # def delete_product(self, product_id):
    #     """This method deletes a product"""
    #     delete_item = self.dbconn.delete_product(product_id=product_id)
    #     if delete_item:
    #         return True
    #     return False
