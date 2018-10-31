from app.db.databmanager import DatabaseConnection 

class DBMethods:
    def __init__(self):
        self.connect = DatabaseConnection()
        self.cursor = self.connect.dict_cursor

    def add_new_user(self, username, phone, role, password):
        """This method registers a user"""
        query = (
            """INSERT INTO users (username, phone, role, password) 
               VALUES ('{}', '{}', '{}', '{}')""".format(username, phone, role, password))
        self.cursor.execute(query)

    def does_username_exist(self,username):
        """
        This method checks whether there's an existing username
        """
        query = ("""SELECT * FROM users where username = '{}'""".format(username))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        if user:
            return user
        return False    

    def does_phone_exist(self,phone):
        """
        This method checks whether there's an existing phone
        """
        query = ("""SELECT * FROM users where phone = '{}'""".format(phone))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        if user:
            return True
        return False        

    def user_login(self, username, password):
        """This method checks for user login"""
        query = ("""SELECT * from users where username = '{}' and password='{}'""".format(username, password))
        self.cursor.execute(query)
        user =self.cursor.fetchone()
        return user

    def add_new_product(self, product, quantity, price, reg_date):
        """This method adds new product item"""
        query = (
            """INSERT INTO products (product, quantity, price, reg_date) VALUES ('{}', '{}', '{}', '{}')""".
            format(product, quantity, price, reg_date))
        self.cursor.execute(query)

    def does_product_exist(self,product):
        """This method checks whether product exists"""
        query = ("""SELECT * FROM products where product = '{}'""".format(product))
        self.cursor.execute(query)
        product = self.cursor.fetchone()
        if product:
            return product
        return False

    def update_product(self, product, quantity, price, product_id, reg_date):
        """This method updates the product"""
        try:
            query = ("""UPDATE products SET product = '{}', quantity = '{}', price = '{}', reg_date = '{}' where product_id = '{}'""" .format(
                product, quantity, price, product_id, reg_date ))
            self.cursor.execute(query)
            count = self.cursor.rowcount
            if int(count) > 0:
                return True
            else:
                return False   
        except:
            return False

    def get_single_product(self,product_id):
        """This method gets a single product"""
        self.cursor.execute("SELECT * FROM products WHERE product_id = '{}'" .format(product_id))
        row = self.cursor.fetchone()
        return row

    def get_all_products(self):
        """This method gets all products being added"""
        self.cursor.execute("SELECT * from products")
        all_products = self.cursor.fetchall()
        return all_products     

    def delete_product(self, product_id):
        """This method deletes a specific product"""
        query = ("""DELETE FROM products WHERE product_id = '{}'""" .format(product_id))
        self.cursor.execute(query)
        delete = self.cursor.rowcount
        if int(delete) > 0:
            return True
        else:
            return False 

    def create_sale_record(self, product, quantity, amount, attendant, date):
        """This method creates a sale record"""
        query = (
            """INSERT INTO sales (product, quantity, amount, attendant, date) 
               VALUES ('{}', '{}', '{}', '{}', '{}')""".format(product, quantity, amount, attendant, date))
        self.cursor.execute(query)
    
    def get_new_sale(self):
        """This method gets the most recent sale record being made """ 
        self.cursor.execute("SELECT * FROM sales ORDER BY sale_id DESC LIMIT 1")
        new_record = self.cursor.fetchall()
        return new_record

    def get_all_sales(self):
        """This method gets all available sales"""
        self.cursor.execute("SELECT * from sales")
        all_sales = self.cursor.fetchall()
        return all_sales

    def get_all_sales_for_user(self, username):
        """This method gets all available sales"""
        self.cursor.execute("SELECT * FROM sales WHERE attendant = '{}'" .format(username))
        sale_record = self.cursor.fetchall()
        return sale_record   