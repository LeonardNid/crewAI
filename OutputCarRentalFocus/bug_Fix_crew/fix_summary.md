{
  "models": {
    "file_path": "Output/backendCrew/models.json",
    "patch": [
      {
        "op": "replace",
        "path": "/topic",
        "value": "Car Rental Service",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/models/0/to_dict",
        "value": "def to_dict(self):\n    return {\n        'id': self.id,\n        'brand': self.brand,\n        'model': self.model,\n        'category': self.category,\n        'status': self.status,\n        'plate_no': self.plate_no,\n        'location_id': self.location_id,\n        'price_per_day': float(self.price_per_day) if self.price_per_day is not None else None\n    }",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/models/2/to_dict",
        "value": "def to_dict(self):\n    from email.utils import formatdate\n    import datetime\n\n    def fmt_date(d):\n        if not d:\n            return None\n        if isinstance(d, str):\n            try:\n                d = datetime.datetime.strptime(d, '%Y-%m-%d').date()\n            except Exception:\n                return d\n        dt = datetime.datetime.combine(d, datetime.time.min).replace(tzinfo=datetime.timezone.utc)\n        return formatdate(dt.timestamp(), usegmt=True)\n\n    return {\n        'id': self.id,\n        'customer_id': self.customer_id,\n        'car_id': self.car_id,\n        'start_date': fmt_date(self.start_date),\n        'end_date': fmt_date(self.end_date),\n        'status': self.status,\n        'total_price': float(self.total_price) if self.total_price is not None else None\n    }",
        "from_path": null
      }
    ]
  },
  "routes": {
    "file_path": "Output/backendCrew/routes.json",
    "patch": [
      {
        "op": "replace",
        "path": "/topic",
        "value": "Car Rental Service",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/5/branches/POST",
        "value": "from decimal import Decimal, ROUND_HALF_UP\nfrom datetime import datetime\n\ndata = request.get_json()\ncar = Car.query.get(data.get('car_id'))\nif not car:\n    return jsonify({\"message\": \"Car not found\"}), 404\n\nrequired_fields = ['customer_id', 'start_date', 'end_date']\nfor field in required_fields:\n    if not data.get(field):\n        return jsonify({\"message\": f\"{field} is required\"}), 400\n\nstart_date = data.get('start_date')\nend_date = data.get('end_date')\n\n# Robust date parsing\ntry:\n    if isinstance(start_date, str):\n        start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()\n    elif isinstance(start_date, datetime.date):\n        start_dt = start_date\n    else:\n        return jsonify({\"message\": \"Invalid start_date format\"}), 400\n\n    if isinstance(end_date, str):\n        end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()\n    elif isinstance(end_date, datetime.date):\n        end_dt = end_date\n    else:\n        return jsonify({\"message\": \"Invalid end_date format\"}), 400\nexcept ValueError:\n    return jsonify({\"message\": \"Invalid date format, expected YYYY-MM-DD\"}), 400\n\nif (end_dt - start_dt).days < 0:\n    return jsonify({\"message\": \"End date must be after start date\"}), 400\n\n# Check overlapping rentals\noverlapping_rental = Rental.query.filter(\n    Rental.car_id == car.id,\n    Rental.status != 'completed',\n    Rental.start_date <= end_dt,\n    Rental.end_date >= start_dt\n).first()\nif overlapping_rental:\n    return jsonify({\"message\": \"Car is not available for the requested period\"}), 400\n\nrental_days = (end_dt - start_dt).days + 1\nprice_per_day = car.price_per_day\nif price_per_day is None:\n    return jsonify({\"message\": \"Car price not set\"}), 400\n\nrental_status = data.get('status', 'rented')\nif rental_status not in ['rented', 'reserved', 'booked']:\n    rental_status = 'rented'\n\n# Use Decimal for accurate price computations\nprice_per_day_dec = Decimal(str(price_per_day))\nrental_days_dec = Decimal(rental_days)\ntotal_price = (price_per_day_dec * rental_days_dec).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)\n\nnew_obj = Rental(\n    customer_id=data.get('customer_id'),\n    car_id=car.id,\n    start_date=start_dt,\n    end_date=end_dt,\n    status=rental_status,\n    total_price=total_price\n)\ndb.session.add(new_obj)\nif rental_status in ['rented', 'booked', 'reserved']:\n    car.status = 'rented'\nelse:\n    car.status = 'available'\ndb.session.commit()\nreturn jsonify(new_obj.to_dict()), 201",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/6/branches/PUT",
        "value": "from decimal import Decimal, ROUND_HALF_UP\nimport datetime\n\ndef parse_date(d):\n    if isinstance(d, str):\n        try:\n            return datetime.datetime.strptime(d, '%Y-%m-%d').date()\n        except ValueError:\n            return None\n    elif isinstance(d, datetime.date):\n        return d\n    return None\n\ndata = request.get_json()\nobj = Rental.query.get(id)\nif not obj:\n    return jsonify({\"message\": \"Rental not found\"}), 404\n\nif 'start_date' in data:\n    parsed_start = parse_date(data['start_date'])\n    if parsed_start is None:\n        return jsonify({\"message\": \"Invalid start_date format\"}), 400\n    data['start_date'] = parsed_start\nif 'end_date' in data:\n    parsed_end = parse_date(data['end_date'])\n    if parsed_end is None:\n        return jsonify({\"message\": \"Invalid end_date format\"}), 400\n    data['end_date'] = parsed_end\n\nstart_date = data.get('start_date', obj.start_date)\nend_date = data.get('end_date', obj.end_date)\n\nif (end_date - start_date).days < 0:\n    return jsonify({\"message\": \"End date must be after start date\"}), 400\n\n# Check overlapping rentals excluding itself\noverlapping_rental = Rental.query.filter(\n    Rental.car_id == obj.car_id,\n    Rental.id != obj.id,\n    Rental.status != 'completed',\n    Rental.start_date <= end_date,\n    Rental.end_date >= start_date\n).first()\nif overlapping_rental:\n    return jsonify({\"message\": \"Car is not available for the requested period\"}), 400\n\n# Update attributes from incoming data except total_price\nfor k, v in data.items():\n    if k != 'total_price':\n        setattr(obj, k, v)\n\nrental_days = (end_date - start_date).days + 1\ncar = Car.query.get(obj.car_id)\nif not car:\n    return jsonify({\"message\": \"Car not found\"}), 404\nprice_per_day = car.price_per_day\nif price_per_day is None:\n    return jsonify({\"message\": \"Car price not set\"}), 400\n\nprice_per_day_dec = Decimal(str(price_per_day))\nrental_days_dec = Decimal(rental_days)\ntotal_price = (price_per_day_dec * rental_days_dec).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)\n\nobj.total_price = total_price\n\nif 'status' in data:\n    if obj.status in ['rented', 'booked', 'reserved']:\n        car.status = 'rented'\n    elif obj.status in ['completed', 'cancelled']:\n        car.status = 'available'\n\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/7/branches/POST",
        "value": "obj = Rental.query.get(id)\nif not obj:\n    return jsonify({\"message\": \"Rental not found\"}), 404\n# Mark rental as returned and completed\nobj.status = 'completed'\n# Update car status to available\ncar = Car.query.get(obj.car_id)\nif car:\n    car.status = 'available'\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/0/branches/POST",
        "value": "data = request.get_json()\nnew_obj = Car(**data)\ndb.session.add(new_obj)\ndb.session.commit()\nreturn jsonify(new_obj.to_dict()), 201",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/1/branches/PUT",
        "value": "obj = Car.query.get(id)\nif not obj:\n    return jsonify({\"message\": \"Car not found\"}), 404\ndata = request.get_json()\nfor k, v in data.items():\n    setattr(obj, k, v)\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      }
    ]
  }
}