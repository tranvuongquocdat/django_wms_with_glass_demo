from sqlalchemy import select, create_engine, MetaData, Table, insert
from datetime import datetime

class Section_manager():
    def __init__(self):
        self.user_id = None
        self.vendor = None
        self.customer_id = None

        # Kết nối tới cơ sở dữ liệu SQLite
        self.engine = create_engine('sqlite:///db.sqlite3')

        # Khởi tạo đối tượng MetaData
        self.metadata = MetaData()

        # Phản chiếu schema từ cơ sở dữ liệu
        self.metadata.reflect(bind=self.engine)

        # Access the auth_user table
        self.auth_user = Table('auth_user', self.metadata, autoload_with=self.engine)
        self.main_customer = Table('main_customer', self.metadata, autoload_with=self.engine)
        self.main_vendor = Table('main_vendor', self.metadata, autoload_with=self.engine)
        self.main_product = Table('main_product', self.metadata, autoload_with=self.engine)
        self.main_purchase = Table('main_purchase', self.metadata, autoload_with=self.engine)
        self.main_sale = Table('main_sale', self.metadata, autoload_with=self.engine)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_vendor_id(self, vendor_id):
        self.vendor_id = vendor_id

    def set_customer_id(self, customer_id):
        self.customer_id = customer_id

    def insert_purchase_data(self, product_id, quantity=1.0, price=500.0):
        data = {
            'quantity': quantity,
            'price': price,
            'total_amount': quantity * price,
            'purchase_date': datetime.now(),
            'product_id': product_id,
            'vendor_id': self.vendor_id
        }
        
        with self.engine.connect() as conn:
            query = insert(self.main_purchase).values(data)
            conn.execute(query)
            conn.commit()

    def insert_sale_data(self, product_id, quantity=1.0, price=500.0):
        data = {
            'quantity': quantity,
            'price': price,
            'total_amount': quantity * price,
            'sale_date': datetime.now(),
            'product_id': product_id,
            'customer_id': self.customer_id
        }
        
        with self.engine.connect() as conn:
            query = insert(self.main_sale).values(data)
            conn.execute(query)
            conn.commit()

    def get_user_ids(self):
        with self.engine.connect() as conn:
            # Select the user_id column from the auth_user table
            query = select(self.auth_user.c.id)
            result = conn.execute(query)
            # Fetch all results and return a list of user_ids
            user_ids = [row[0] for row in result.fetchall()]
        return user_ids

    def get_customer_ids(self):
        with self.engine.connect() as conn:
            # Select the id column from the main_customer table
            query = select(self.main_customer.c.id)
            result = conn.execute(query)
            # Fetch all results and return a list of customer_ids
            customer_ids = [row[0] for row in result.fetchall()]
        return customer_ids

    def get_vendor_ids(self):
        with self.engine.connect() as conn:
            # Select the id column from the main_vendor table
            query = select(self.main_vendor.c.id)
            result = conn.execute(query)
            # Fetch all results and return a list of vendor_ids
            vendor_ids = [row[0] for row in result.fetchall()]
        return vendor_ids

    def get_product_ids(self):
        with self.engine.connect() as conn:
            # Select the id column from the main_product table
            query = select(self.main_product.c.id)
            result = conn.execute(query)
            # Fetch all results and return a list of product_ids
            product_ids = [row[0] for row in result.fetchall()]
        return product_ids

