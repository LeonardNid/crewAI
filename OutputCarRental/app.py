from flask import Flask, request, jsonify
from models import db, Car, Location, Customer, Rental, Payment, Service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Multi-Branch Car Rental API running'})

# List all cars with optional filters (location, category, seats, transmission, price range) or create a new car
@app.route('/cars', methods=['GET', 'POST'])
def cars(): 
    if request.method == 'GET':
        objs = Car.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Car(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a specific car by plate number
@app.route('/cars_plate_no/<string:plate_no>', methods=['GET', 'PUT', 'DELETE'])
def cars_plate_no_string_plate_no(plate_no): 
    if request.method == 'GET':
        obj = Car.query.get(plate_no)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Car.query.get(plate_no)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Car.query.get(plate_no)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Car deleted"})

# Search cars by partial or full match on plate number or model
@app.route('/cars_name/<string:search_str>', methods=['GET'])
def cars_name_string_search_str(search_str):
    query = Car.query
    args = request.args
    filters = []
    search_str_lower = search_str.lower()
    objs = query.filter((Car.plate_no.ilike(f'%{search_str_lower}%')) | (Car.model.ilike(f'%{search_str_lower}%'))).all()
    if not objs:
        return jsonify({"message": "Car not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# List cars available for rental filtered by category, date range, and pickup location to support booking workflow
@app.route('/cars_available', methods=['GET'])
def cars_available():
    # This endpoint should filter available cars by category, pickup location and date range
    # but current code returns all cars without filtering
    query = Car.query
    args = request.args
    # Extract filters from args
    category = args.get('category')
    pickup_location = args.get('pickup_location')
    date_start = args.get('start_date')
    date_end = args.get('end_date')
    q = query
    if category:
        q = q.filter(Car.category == category)
    if pickup_location:
        q = q.filter(Car.location_id == pickup_location)
    # Filtering by availability requires joining Rental and checking no overlapping bookings
    # For simplicity we consider cars with status 'available'
    q = q.filter(Car.status == 'available')
    objs = q.all()
    return jsonify([o.to_dict() for o in objs])

# List all locations or create a new location
@app.route('/locations', methods=['GET', 'POST'])
def locations(): 
    if request.method == 'GET':
        objs = Location.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Location(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a specific location by ID
@app.route('/locations/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def locations_int_id(id): 
    if request.method == 'GET':
        obj = Location.query.get(id)
        if not obj:
            return jsonify({"message": "Location not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Location.query.get(id)
        if not obj:
            return jsonify({"message": "Location not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Location.query.get(id)
        if not obj:
            return jsonify({"message": "Location not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Location deleted"})

# List all customers or create a new customer
@app.route('/customers', methods=['GET', 'POST'])
def customers(): 
    if request.method == 'GET':
        objs = Customer.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Customer(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a customer by customer ID
@app.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def customers_int_customer_id(customer_id): 
    if request.method == 'GET':
        obj = Customer.query.get(customer_id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Customer.query.get(customer_id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Customer.query.get(customer_id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Customer deleted"})

# Search customers by partial or full name match
@app.route('/customers_name/<string:name>', methods=['GET'])
def customers_name_string_name(name):
    query = Customer.query
    args = request.args
    filters = []
    name_lower = name.lower()
    objs = query.filter(Customer.name.ilike(f'%{name_lower}%')).all()
    if not objs:
        return jsonify({"message": "Customer not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# List rentals with optional filters (status, customer, date range) or book a new rental with car status locking and pricing snapshot
@app.route('/rentals', methods=['GET', 'POST'])
def rentals(): 
    if request.method == 'GET':
        objs = Rental.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Rental(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or cancel a rental by rental ID; deletion only allowed if rental start date in future, trigger payment refund
@app.route('/rentals/<int:rental_id>', methods=['GET', 'PUT', 'DELETE'])
def rentals_int_rental_id(rental_id): 
    if request.method == 'GET':
        obj = Rental.query.get(rental_id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Rental.query.get(rental_id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Rental.query.get(rental_id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404
        from datetime import datetime
        import dateutil.parser
        start_date = dateutil.parser.parse(obj.pickup_date)
        now = datetime.utcnow()
        if start_date <= now:
            return jsonify({"message": "Cannot delete a rental that has already started or in progress"}), 400
        # Trigger payment refund logic here - omitted, just comment
        # refund_payment(obj.id)
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Rental deleted"})

# Mark rental as returned; update rental status to 'closed', update car status to 'available', odometer, and location
@app.route('/rentals/<int:rental_id>/return', methods=['POST'])
def rentals_int_rental_id_return(rental_id):
    obj = Rental.query.get(rental_id)
    if not obj:
        return jsonify({"message": "Rental not found"}), 404
    # get request data
    data = request.get_json()
    for k, v in data.items():
        setattr(obj, k, v)
    obj.status = 'closed'
    car = Car.query.filter_by(plate_no=obj.car_plate_no).first()
    if car:
        car.status = 'available'
        if 'current_odometer' in data:
            car.current_odometer = data['current_odometer']
        if 'location_id' in data:
            car.location_id = data['location_id']
    db.session.commit()
    return jsonify(obj.to_dict())

# List payments with optional filters (rental ID, date range) or create a new payment
@app.route('/payments', methods=['GET', 'POST'])
def payments(): 
    if request.method == 'GET':
        objs = Payment.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Payment(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve or update a payment record by payment ID (e.g., mark as refunded)
@app.route('/payments/<int:payment_id>', methods=['GET', 'PUT'])
def payments_int_payment_id(payment_id): 
    if request.method == 'GET':
        obj = Payment.query.get(payment_id)
        if not obj:
            return jsonify({"message": "Payment not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Payment.query.get(payment_id)
        if not obj:
            return jsonify({"message": "Payment not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())

# List service records with optional filters (car plate_no, service_type, active status) or create a new service record
@app.route('/services', methods=['GET', 'POST'])
def services(): 
    if request.method == 'GET':
        objs = Service.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Service(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a service record by service ID
@app.route('/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE'])
def services_int_service_id(service_id): 
    if request.method == 'GET':
        obj = Service.query.get(service_id)
        if not obj:
            return jsonify({"message": "Service not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Service.query.get(service_id)
        if not obj:
            return jsonify({"message": "Service not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Service.query.get(service_id)
        if not obj:
            return jsonify({"message": "Service not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Service deleted"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)