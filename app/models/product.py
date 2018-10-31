class Product(object):
    """This class handles class model"""
    
    def __init__(self, product_name, quantity, price, reg_date):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.reg_date=reg_date