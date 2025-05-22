from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = "cars"
    plate_no = db.Column(db.String(20), primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    category = db.Column(db.String(30))
    seats = db.Column(db.Integer)
    transmission = db.Column(db.String(15))
    fuel_type = db.Column(db.String(20))
    daily_rate = db.Column(db.Numeric(10,2))
    current_odometer = db.Column(db.Integer)
    status = db.Column(db.String(20))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship(
        'Location',
        back_populates='cars',
        lazy=True
    )
    rentals = db.relationship(
    'Rental',
    back_populates='car',
    lazy=True,
    cascade="all, delete-orphan"
    )
    services = db.relationship(
    'Service',
    back_populates='car',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "plate_no": self.plate_no,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "category": self.category,
            "seats": self.seats,
            "transmission": self.transmission,
            "fuel_type": self.fuel_type,
            "daily_rate": self.daily_rate,
            "current_odometer": self.current_odometer,
            "status": self.status,
            "location_id": self.location_id
        }

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    street = db.Column(db.String(150))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(50))
    phone = db.Column(db.String(30))
    cars = db.relationship(
        'Car',
        back_populates='location',
        lazy=True,
        cascade="all, delete-orphan"
    )
    pickup_rentals = db.relationship(
        'Rental',
        back_populates='pickup_location',
        foreign_keys='Rental.pickup_location_id',
        lazy=True
    )
    dropoff_rentals = db.relationship(
        'Rental',
        back_populates='dropoff_location',
        foreign_keys='Rental.dropoff_location_id',
        lazy=True
    )
    rentals = db.relationship(
        'Rental',
        primaryjoin="or_(Location.id==Rental.pickup_location_id, Location.id==Rental.dropoff_location_id)",
        foreign_keys=[Rental.pickup_location_id, Rental.dropoff_location_id],
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "phone": self.phone
        }

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    driver_license_no = db.Column(db.String(50))
    license_expiry = db.Column(db.Date)
    vip = db.Column(db.Boolean)
    rentals = db.relationship(
    'Rental',
    back_populates='customer',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "driver_license_no": self.driver_license_no,
            "license_expiry": self.license_expiry,
            "vip": self.vip
        }

class Rental(db.Model):
    __tablename__ = "rentals"
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_plate_no = db.Column(db.String(20), db.ForeignKey('cars.plate_no'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    pickup_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    dropoff_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    pickup_date = db.Column(db.DateTime)
    dropoff_date = db.Column(db.DateTime)
    daily_rate_snapshot = db.Column(db.Numeric(10,2))
    total_price = db.Column(db.Numeric(10,2))
    status = db.Column(db.String(20))
    car = db.relationship(
        'Car',
        back_populates='rentals',
        lazy=True
    )
    customer = db.relationship(
        'Customer',
        back_populates='rentals',
        lazy=True
    )
    pickup_location = db.relationship(
        'Location',
        back_populates='pickup_rentals',
        foreign_keys=[pickup_location_id],
        lazy=True
    )
    dropoff_location = db.relationship(
        'Location',
        back_populates='dropoff_rentals',
        foreign_keys=[dropoff_location_id],
        lazy=True
    )
    payments = db.relationship(
        'Payment',
        back_populates='rental',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "rental_id": self.rental_id,
            "car_plate_no": self.car_plate_no,
            "customer_id": self.customer_id,
            "pickup_location_id": self.pickup_location_id,
            "dropoff_location_id": self.dropoff_location_id,
            "pickup_date": self.pickup_date,
            "dropoff_date": self.dropoff_date,
            "daily_rate_snapshot": self.daily_rate_snapshot,
            "total_price": self.total_price,
            "status": self.status
        }

class Payment(db.Model):
    __tablename__ = "payments"
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.rental_id'))
    amount = db.Column(db.Numeric(10,2))
    method = db.Column(db.String(30))
    paid_at = db.Column(db.DateTime)
    refunded = db.Column(db.Boolean)
    rental = db.relationship(
        'Rental',
        back_populates='payments',
        lazy=True
    )

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "rental_id": self.rental_id,
            "amount": self.amount,
            "method": self.method,
            "paid_at": self.paid_at,
            "refunded": self.refunded
        }

class Service(db.Model):
    __tablename__ = "services"
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_plate_no = db.Column(db.String(20), db.ForeignKey('cars.plate_no'))
    service_type = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    cost = db.Column(db.Numeric(10,2))
    notes = db.Column(db.Text)
    car = db.relationship(
        'Car',
        back_populates='services',
        lazy=True
    )

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "car_plate_no": self.car_plate_no,
            "service_type": self.service_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cost": self.cost,
            "notes": self.notes
        }

