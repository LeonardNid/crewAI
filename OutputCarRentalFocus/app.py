from flask import Flask, request, jsonify
from models import db, Car, Customer, Rental, Location

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Car Rental Service API running'})

# List all cars or create a new car
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

# Retrieve, update, or delete a specific car by ID
@app.route('/cars/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def cars_int_id(id): 
    if request.method == 'GET':
        obj = Car.query.get(id)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Car.query.get(id)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Car.query.get(id)
        if not obj:
            return jsonify({"message": "Car not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Car deleted"})

# List all available cars filtered by category, location, start_date, and end_date using query parameters
@app.route('/cars_available', methods=['GET'])
def cars_available():
    from datetime import datetime

    category = request.args.get('category')
    location_id = request.args.get('location')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Car.query.filter(Car.status == 'available')
    if category:
        query = query.filter(Car.category == category)
    if location_id:
        query = query.filter(Car.location_id == int(location_id))

    if start_date and end_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        # Exclude cars that have rentals overlapping the requested period
        subquery = db.session.query(Rental.car_id).filter(
            Rental.status != 'completed',
            Rental.start_date <= end_date_obj,
            Rental.end_date >= start_date_obj
        ).subquery()
        query = query.filter(~Car.id.in_(subquery))

    objs = query.all()
    return jsonify([o.to_dict() for o in objs])

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

# Retrieve, update, or delete a specific customer by ID
@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customers_int_id(id): 
    if request.method == 'GET':
        obj = Customer.query.get(id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Customer.query.get(id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Customer.query.get(id)
        if not obj:
            return jsonify({"message": "Customer not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Customer deleted"})

# List all rentals or create a new rental with availability check, total_price calculation (price_per_day * rental days), and car status update (to rented)
@app.route('/rentals', methods=['GET', 'POST'])
def rentals(): 
    if request.method == 'GET':
        objs = Rental.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from decimal import Decimal, ROUND_HALF_UP
        from datetime import datetime

        data = request.get_json()
        car = Car.query.get(data.get('car_id'))
        if not car:
            return jsonify({"message": "Car not found"}), 404

        required_fields = ['customer_id', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"{field} is required"}), 400

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Robust date parsing
        try:
            if isinstance(start_date, str):
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            elif isinstance(start_date, datetime.date):
                start_dt = start_date
            else:
                return jsonify({"message": "Invalid start_date format"}), 400

            if isinstance(end_date, str):
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            elif isinstance(end_date, datetime.date):
                end_dt = end_date
            else:
                return jsonify({"message": "Invalid end_date format"}), 400
        except ValueError:
            return jsonify({"message": "Invalid date format, expected YYYY-MM-DD"}), 400

        if (end_dt - start_dt).days < 0:
            return jsonify({"message": "End date must be after start date"}), 400

        # Check overlapping rentals
        overlapping_rental = Rental.query.filter(
            Rental.car_id == car.id,
            Rental.status != 'completed',
            Rental.start_date <= end_dt,
            Rental.end_date >= start_dt
        ).first()
        if overlapping_rental:
            return jsonify({"message": "Car is not available for the requested period"}), 400

        rental_days = (end_dt - start_dt).days + 1
        price_per_day = car.price_per_day
        if price_per_day is None:
            return jsonify({"message": "Car price not set"}), 400

        rental_status = data.get('status', 'rented')
        if rental_status not in ['rented', 'reserved', 'booked']:
            rental_status = 'rented'

        # Use Decimal for accurate price computations
        price_per_day_dec = Decimal(str(price_per_day))
        rental_days_dec = Decimal(rental_days)
        total_price = (price_per_day_dec * rental_days_dec).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        new_obj = Rental(
            customer_id=data.get('customer_id'),
            car_id=car.id,
            start_date=start_dt,
            end_date=end_dt,
            status=rental_status,
            total_price=total_price
        )
        db.session.add(new_obj)
        if rental_status in ['rented', 'booked', 'reserved']:
            car.status = 'rented'
        else:
            car.status = 'available'
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update (including total_price and status), or cancel a rental by ID only if rental period not started; triggers refund process before deletion
@app.route('/rentals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def rentals_int_id(id): 
    if request.method == 'GET':
        obj = Rental.query.get(id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        from decimal import Decimal, ROUND_HALF_UP
        import datetime

        def parse_date(d):
            if isinstance(d, str):
                try:
                    return datetime.datetime.strptime(d, '%Y-%m-%d').date()
                except ValueError:
                    return None
            elif isinstance(d, datetime.date):
                return d
            return None

        data = request.get_json()
        obj = Rental.query.get(id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404

        if 'start_date' in data:
            parsed_start = parse_date(data['start_date'])
            if parsed_start is None:
                return jsonify({"message": "Invalid start_date format"}), 400
            data['start_date'] = parsed_start
        if 'end_date' in data:
            parsed_end = parse_date(data['end_date'])
            if parsed_end is None:
                return jsonify({"message": "Invalid end_date format"}), 400
            data['end_date'] = parsed_end

        start_date = data.get('start_date', obj.start_date)
        end_date = data.get('end_date', obj.end_date)

        if (end_date - start_date).days < 0:
            return jsonify({"message": "End date must be after start date"}), 400

        # Check overlapping rentals excluding itself
        overlapping_rental = Rental.query.filter(
            Rental.car_id == obj.car_id,
            Rental.id != obj.id,
            Rental.status != 'completed',
            Rental.start_date <= end_date,
            Rental.end_date >= start_date
        ).first()
        if overlapping_rental:
            return jsonify({"message": "Car is not available for the requested period"}), 400

        # Update attributes from incoming data except total_price
        for k, v in data.items():
            if k != 'total_price':
                setattr(obj, k, v)

        rental_days = (end_date - start_date).days + 1
        car = Car.query.get(obj.car_id)
        if not car:
            return jsonify({"message": "Car not found"}), 404
        price_per_day = car.price_per_day
        if price_per_day is None:
            return jsonify({"message": "Car price not set"}), 400

        price_per_day_dec = Decimal(str(price_per_day))
        rental_days_dec = Decimal(rental_days)
        total_price = (price_per_day_dec * rental_days_dec).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        obj.total_price = total_price

        if 'status' in data:
            if obj.status in ['rented', 'booked', 'reserved']:
                car.status = 'rented'
            elif obj.status in ['completed', 'cancelled']:
                car.status = 'available'

        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Rental.query.get(id)
        if not obj:
            return jsonify({"message": "Rental not found"}), 404

        import datetime
        now = datetime.datetime.now().date()
        rental_start = obj.start_date if isinstance(obj.start_date, datetime.date) else datetime.datetime.strptime(obj.start_date, '%Y-%m-%d').date()
        # Business rule forbids cancellation after start date
        if rental_start <= now:
            return jsonify({"message": "Cannot cancel rental after start date"}), 400

        # Trigger refund process here (placeholder)

        car = Car.query.get(obj.car_id)
        if car:
            car.status = 'available'
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Rental deleted"})

# Mark a rental as returned and completed; update rental and car status accordingly
@app.route('/rentals/<int:id>/return', methods=['POST'])
def rentals_int_id_return(id):
    obj = Rental.query.get(id)
    if not obj:
        return jsonify({"message": "Rental not found"}), 404
    # Mark rental as returned and completed
    obj.status = 'completed'
    # Update car status to available
    car = Car.query.get(obj.car_id)
    if car:
        car.status = 'available'
    db.session.commit()
    return jsonify(obj.to_dict())

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

# Retrieve, update, or delete a specific location by ID
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

# Retrieve aggregated monthly revenue summary analytics
@app.route('/analytics_revenue_monthly', methods=['GET'])
def analytics_revenue_monthly():
    from sqlalchemy import extract, func
    import datetime

    # Generate monthly revenue summary
    results = db.session.query(
        extract('year', Rental.start_date).label('year'),
        extract('month', Rental.start_date).label('month'),
        func.sum(Rental.total_price).label('total_revenue')
    ).group_by('year', 'month').all()

    response = []
    for r in results:
        response.append({
            'year': int(r.year),
            'month': int(r.month),
            'total_revenue': float(r.total_revenue)
        })

    return jsonify(response)

# Retrieve utilization rate per car category analytics
@app.route('/analytics_utilization_car_category', methods=['GET'])
def analytics_utilization_car_category():
    from sqlalchemy import func
    import datetime

    # Retrieve utilization rate per car category

    cars = Car.query.all()
    rental_durations = {}
    category_counts = {}

    for car in cars:
        category = car.category
        category_counts[category] = category_counts.get(category, 0) + 1

        rentals = Rental.query.filter(Rental.car_id == car.id).all()
        total_days = 0
        for r in rentals:
            start_dt = r.start_date if isinstance(r.start_date, datetime.date) else datetime.datetime.strptime(r.start_date, '%Y-%m-%d').date()
            end_dt = r.end_date if isinstance(r.end_date, datetime.date) else datetime.datetime.strptime(r.end_date, '%Y-%m-%d').date()
            days = (end_dt - start_dt).days + 1
            total_days += max(days, 0)

        rental_durations[category] = rental_durations.get(category, 0) + total_days

    # Assuming utilization rate as total rental days / (number of cars in category * 30 days month as approximation)
    response = []
    for category in category_counts:
        cars_in_cat = category_counts[category]
        total_rental_days = rental_durations.get(category, 0)
        utilization_rate = total_rental_days / (cars_in_cat * 30) if cars_in_cat > 0 else 0
        response.append({
            'category': category,
            'utilization_rate': round(utilization_rate, 4)
        })

    return jsonify(response)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)