from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    plate_no = db.Column(db.String(20), unique=True, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    price_per_day = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.relationship(
        'Location',
        back_populates='cars',
        lazy=True
    )
    rentals = db.relationship(
        'Rental',
        back_populates='car',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "category": self.category,
            "status": self.status,
            "plate_no": self.plate_no,
            "location_id": self.location_id,
            "price_per_day": self.price_per_day
        }

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    rentals = db.relationship(
        'Rental',
        back_populates='customer',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    customer = db.relationship(
        'Customer',
        back_populates='rentals',
        lazy=True
    )
    car = db.relationship(
        'Car',
        back_populates='rentals',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "car_id": self.car_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_price": self.total_price,
            "status": self.status
        }

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    cars = db.relationship(
        'Car',
        back_populates='location',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

