from app import db
from sqlalchemy import CheckConstraint
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.String(50), primary_key=True)
    first_order_date = db.Column(db.Date)
    last_order_date = db.Column(db.Date)
    signup_date = db.Column(db.Date, nullable=True)
    customer_city = db.Column(db.String(100))
    customer_state = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    inventory = db.relationship('Inventory', backref='product', uselist=False)

class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.String(50), primary_key=True)
    customer_id = db.Column(db.String(50), db.ForeignKey('customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_status = db.Column(db.String(20), nullable=False)  # created, paid, shipped, delivered, canceled, refunded
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)  # paid, pending, failed, refunded
    
    __table_args__ = (
        CheckConstraint('payment_amount >= 0', name='check_payment_amount_positive'),
    )
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String(50), db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # captured at time of sale
    discount = db.Column(db.Numeric(10, 2), default=0)  # absolute per line
    
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('unit_price >= 0', name='check_unit_price_positive'),
        CheckConstraint('discount >= 0', name='check_discount_positive'),
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    on_hand_qty = db.Column(db.Integer, nullable=False, default=0)
    reorder_point = db.Column(db.Integer, nullable=False, default=0)
    reorder_qty = db.Column(db.Integer, nullable=False, default=0)
