from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import and_

database = SQLAlchemy()


class ProductCategory(database.Model):
    __tablename__ = "productcategory"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    categoryId = database.Column(database.Integer, database.ForeignKey("categories.id"), nullable=False)


class ProductOrder(database.Model):
    __tablename__ = "productorder"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    orderId = database.Column(database.Integer, database.ForeignKey("orders.id"), nullable=False)
    price = database.Column(database.Float, nullable=False)
    received = database.Column(database.Integer, nullable=False)
    requested = database.Column(database.Integer, nullable=False)

    def to_dict(self):
        product = Product.query.filter(Product.id == self.productId).first()
        return {
            "categories": [category.name for category in product.categories],
            "name": product.name,
            "price": self.price,
            "received": self.received,
            "requested": self.requested
        }

    def __repr__(self):
        return "({}, {}, {}, {}, {})".format(self.id, self.productId, self.orderId, self.received, self.requested)


class Product(database.Model):
    __tablename__ = "products"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    price = database.Column(database.Float, nullable=False)
    quantity = database.Column(database.Integer, nullable=False)

    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    orders = database.relationship("Order", secondary=ProductOrder.__table__, back_populates="products")

    def get_pending_product_orders(self):
        return ProductOrder.query.join(Order).filter(
            and_(
                ProductOrder.productId == self.id,
                ProductOrder.requested != ProductOrder.received
            )
        ).order_by(Order.timestamp).all()

    def __repr__(self):
        return "({}, {}, {}, {}, {})".format(self.id, self.name, self.price, self.quantity, str(self.categories))


class Category(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    numberOfSoldProducts = database.Column(database.Integer, nullable=False)

    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")

    def __repr__(self):
        return self.name


class OrderStatus(database.Model):
    __tablename__ = "orderstatus"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)

    orders = database.relationship("Order", back_populates="status")

    def __repr__(self):
        return self.name


class Order(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.Integer, primary_key=True)
    timestamp = database.Column(database.DateTime(timezone=True), server_default=func.now(), nullable=False)
    userEmail = database.Column(database.String(256), nullable=False)

    statusId = database.Column(database.Integer, database.ForeignKey("orderstatus.id"), nullable=False)
    status = database.relationship("OrderStatus", back_populates="orders")

    products = database.relationship("Product", secondary=ProductOrder.__table__, back_populates="orders")

    def get_product_orders(self):
        return ProductOrder.query.filter(ProductOrder.orderId == self.id).all()

    def __repr__(self):
        return "({}, {}, {}, {}, {}, {})".format(self.id, self.price, self.timestamp.isoformat(), self.userEmail, self.status.name, str(self.products))
