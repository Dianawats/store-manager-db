# model class for a sale record
from app.models.product import Product
class Sale(Product):
    """
    This is a sale class that inherits from the product
    """

    def __init__(self,product_name,quantity,price,attendant,date):
        super(Sale, self).__init__(product_name, quantity, price)
        self.attendant = attendant
        self.date = date