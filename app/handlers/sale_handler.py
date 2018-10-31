from app.db.database_methods import DBMethods
from app.models.sale import Sale


class SaleHandler:
    """This class controls sale"""
    def __init__(self):
        self.dbconn = DBMethods()

    def add_sale_record(self, product_id, quantity, attendant, date):
        """Method for creating a sale record"""

        item = self.dbconn.fetch_single_product(product_id=product_id)
        if item:
            product = item["product"]
            _quantity = int(quantity)
            amount = (item["price"]*int(quantity))
            _attendant = attendant
            _date = date
            new_sale = Sale(product_name=product, quantity=_quantity,
                            price=amount, attendant=_attendant, date=_date)
            self.dbconn.create_sale_record(product=new_sale.product_name, quantity=new_sale.quantity,
                                          amount=new_sale.price, attendant=new_sale.attendant, date=new_sale.date)
            new_quantity = int(item["quantity"])- _quantity
            self.dbconn.update_product(product=product, quantity=new_quantity, price=item["price"], product_id=product_id)
            return True
        else:
            return False

    def get_all_sales(self):
        """Method to get all available sale records"""
        all_sales = self.dbconn.get_all_sales()
        return all_sales

    def get_all_sales_for_user(self, username):
        """Method to get all available sale records for a particular user"""
        all_sales = self.dbconn.get_all_sales_for_user(username=username)
        return all_sales    
