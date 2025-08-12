import os
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.data_dir = "data"
        
    def load_all_data(self):
        """Load all CSV data into the database"""
        try:
            from app import db
            
            # Load in dependency order
            self.load_categories()
            self.load_products()
            self.load_customers()
            self.load_orders()
            self.load_order_items()
            self.load_inventory()
            
            # Create indexes after loading data
            self.create_indexes()
            
            logger.info("All data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def load_categories(self):
        """Load categories from CSV"""
        from app import db
        from models import Category
        
        filepath = os.path.join(self.data_dir, "categories.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Categories file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                category = Category(
                    category_id=int(row['category_id']),
                    category_name=row['category_name']
                )
                db.session.merge(category)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} categories")
    
    def load_products(self):
        """Load products from CSV"""
        from app import db
        from models import Product
        
        filepath = os.path.join(self.data_dir, "products.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Products file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                product = Product(
                    product_id=int(row['product_id']),
                    category_id=int(row['category_id']),
                    product_name=row['product_name'],
                    unit_cost=float(row['unit_cost']),
                    unit_price=float(row['unit_price']),
                    is_active=row.get('is_active', 'true').lower() == 'true'
                )
                db.session.merge(product)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} products")
    
    def load_customers(self):
        """Load customers from CSV"""
        from app import db
        from models import Customer
        
        filepath = os.path.join(self.data_dir, "customers.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Customers file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                customer = Customer(
                    customer_id=row['customer_id'],
                    first_order_date=datetime.strptime(row['first_order_date'], '%Y-%m-%d').date() if row.get('first_order_date') else None,
                    last_order_date=datetime.strptime(row['last_order_date'], '%Y-%m-%d').date() if row.get('last_order_date') else None,
                    signup_date=datetime.strptime(row['signup_date'], '%Y-%m-%d').date() if row.get('signup_date') else None,
                    customer_city=row.get('customer_city'),
                    customer_state=row.get('customer_state'),
                    email=row['email']
                )
                db.session.merge(customer)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} customers")
    
    def load_orders(self):
        """Load orders from CSV"""
        from app import db
        from models import Order
        
        filepath = os.path.join(self.data_dir, "orders.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Orders file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                order = Order(
                    order_id=row['order_id'],
                    customer_id=row['customer_id'],
                    order_date=datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S'),
                    order_status=row['order_status'],
                    payment_amount=float(row['payment_amount']),
                    payment_status=row['payment_status']
                )
                db.session.merge(order)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} orders")
    
    def load_order_items(self):
        """Load order items from CSV"""
        from app import db
        from models import OrderItem
        
        filepath = os.path.join(self.data_dir, "order_items.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Order items file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                order_item = OrderItem(
                    order_id=row['order_id'],
                    product_id=int(row['product_id']),
                    quantity=int(row['quantity']),
                    unit_price=float(row['unit_price']),
                    discount=float(row.get('discount', 0))
                )
                db.session.add(order_item)
                count += 1
                
                if count % 1000 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} order items")
    
    def load_inventory(self):
        """Load inventory from CSV"""
        from app import db
        from models import Inventory
        
        filepath = os.path.join(self.data_dir, "inventory.csv")
        if not os.path.exists(filepath):
            logger.warning(f"Inventory file not found: {filepath}")
            return
            
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            
            for row in reader:
                inventory = Inventory(
                    product_id=int(row['product_id']),
                    on_hand_qty=int(row['on_hand_qty']),
                    reorder_point=int(row['reorder_point']),
                    reorder_qty=int(row['reorder_qty'])
                )
                db.session.merge(inventory)
                count += 1
                
                if count % 100 == 0:
                    db.session.commit()
            
            db.session.commit()
            logger.info(f"Loaded {count} inventory records")
    
    def create_indexes(self):
        """Create database indexes for performance"""
        from app import db
        
        try:
            # Read and execute index creation SQL
            with open("queries/create_indexes.sql", 'r') as f:
                indexes_sql = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in indexes_sql.split(';') if stmt.strip()]
            for statement in statements:
                try:
                    db.session.execute(db.text(statement))
                except Exception as e:
                    # Index might already exist, log warning but continue
                    logger.warning(f"Index creation warning: {str(e)}")
            
            db.session.commit()
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        loader = DataLoader()
        loader.load_all_data()
