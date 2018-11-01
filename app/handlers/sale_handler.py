from app.db.database_methods import DBMethods
from app.models.sale import Sale


class SaleHandler:
    """This class controls sales"""
    def __init__(self):
        self.dbconn = DBMethods()

    def add_sale_record(self, product_id, quantity, attendant, date):
        # creating a sales record
        item = self.dbconn.get_single_product(product_id=product_id)
        if item:
            if item["quantity"] > int(quantity):
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
                self.dbconn.update_product(product=product, quantity=new_quantity, 
                                                            price=item["price"], 
                                                            product_id=product_id)
                return True
            else:
                return False
        return False        

    def get_all_sales(self):
        """This method creates all available sale records"""
        all_sales = self.dbconn.get_all_sales()
        return all_sales

    def get_all_sales_for_user(self, username):
        """This method gets all available sale records for a particular user"""
        all_sales = self.dbconn.get_all_sales_for_user(username=username)
        return all_sales
    
    def get_single_sale(self, sale_id):
        """This method gets a sale record"""
        sale_record = self.dbconn.get_single_sale(sale_id=sale_id)
        return sale_record

    def get_single_sale_for_user(self, sale_id, username):
        """This method gets a sale record for a particular user"""
        sale_record = self.dbconn.get_single_sale_for_user(sale_id=sale_id, username=username)
        return sale_record  

