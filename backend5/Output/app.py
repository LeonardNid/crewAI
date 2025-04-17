from flask import Flask, request, jsonify
from models import db, Frame, Rim, Brakes, Gears, Handlebars, Saddle, Seatpost, BrakePad

# -- CREATE FLASK APP --
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')

def home():
    return jsonify({'message': 'Bicycle Workshop API is Running'})

@app.route('/health')

def health_check():
    return jsonify({'status': 'ok', 'database': db.engine.url})

# Frames Routes
@app.route('/frames', methods=['GET'])
def get_frames():
    frames = Frame.query.all()
    return jsonify([frame.to_dict() for frame in frames]), 200

@app.route('/frames', methods=['POST'])
def create_frame():
    data = request.get_json()
    new_frame = Frame(**data)
    db.session.add(new_frame)
    db.session.commit()
    return jsonify(new_frame.to_dict()), 201

@app.route('/frames/<int:id>', methods=['GET'])
def get_frame(id):
    frame = Frame.query.get(id)
    if not frame:
        return jsonify({'message': 'Frame not found'}), 404
    return jsonify(frame.to_dict()), 200

@app.route('/frames/<int:id>', methods=['PUT'])
def update_frame(id):
    frame = Frame.query.get(id)
    if not frame:
        return jsonify({'message': 'Frame not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(frame, key, value)
    db.session.commit()
    return jsonify(frame.to_dict()), 200

@app.route('/frames/<int:id>', methods=['DELETE'])
def delete_frame(id):
    frame = Frame.query.get(id)
    if not frame:
        return jsonify({'message': 'Frame not found'}), 404
    db.session.delete(frame)
    db.session.commit()
    return jsonify({'message': 'Frame deleted successfully'}), 200

# Rims Routes
@app.route('/rims', methods=['GET'])
def get_rims():
    rims = Rim.query.all()
    return jsonify([rim.to_dict() for rim in rims]), 200

@app.route('/rims', methods=['POST'])
def create_rim():
    data = request.get_json()
    new_rim = Rim(**data)
    db.session.add(new_rim)
    db.session.commit()
    return jsonify(new_rim.to_dict()), 201

@app.route('/rims/<int:id>', methods=['GET'])
def get_rim(id):
    rim = Rim.query.get(id)
    if not rim:
        return jsonify({'message': 'Rim not found'}), 404
    return jsonify(rim.to_dict()), 200

@app.route('/rims/<int:id>', methods=['PUT'])
def update_rim(id):
    rim = Rim.query.get(id)
    if not rim:
        return jsonify({'message': 'Rim not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(rim, key, value)
    db.session.commit()
    return jsonify(rim.to_dict()), 200

@app.route('/rims/<int:id>', methods=['DELETE'])
def delete_rim(id):
    rim = Rim.query.get(id)
    if not rim:
        return jsonify({'message': 'Rim not found'}), 404
    db.session.delete(rim)
    db.session.commit()
    return jsonify({'message': 'Rim deleted successfully'}), 200

# Brakes Routes
@app.route('/brakes', methods=['GET'])
def get_brakes():
    brakes = Brakes.query.all()
    return jsonify([brake.to_dict() for brake in brakes]), 200

@app.route('/brakes', methods=['POST'])
def create_brake():
    data = request.get_json()
    new_brake = Brakes(**data)
    db.session.add(new_brake)
    db.session.commit()
    return jsonify(new_brake.to_dict()), 201

@app.route('/brakes/<int:id>', methods=['GET'])
def get_brake(id):
    brake = Brakes.query.get(id)
    if not brake:
        return jsonify({'message': 'Brake not found'}), 404
    return jsonify(brake.to_dict()), 200

@app.route('/brakes/<int:id>', methods=['PUT'])
def update_brake(id):
    brake = Brakes.query.get(id)
    if not brake:
        return jsonify({'message': 'Brake not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(brake, key, value)
    db.session.commit()
    return jsonify(brake.to_dict()), 200

@app.route('/brakes/<int:id>', methods=['DELETE'])
def delete_brake(id):
    brake = Brakes.query.get(id)
    if not brake:
        return jsonify({'message': 'Brake not found'}), 404
    db.session.delete(brake)
    db.session.commit()
    return jsonify({'message': 'Brake deleted successfully'}), 200

# Gears Routes
@app.route('/gears', methods=['GET'])
def get_gears():
    gears = Gears.query.all()
    return jsonify([gear.to_dict() for gear in gears]), 200

@app.route('/gears', methods=['POST'])
def create_gear():
    data = request.get_json()
    new_gear = Gears(**data)
    db.session.add(new_gear)
    db.session.commit()
    return jsonify(new_gear.to_dict()), 201

@app.route('/gears/<int:id>', methods=['GET'])
def get_gear(id):
    gear = Gears.query.get(id)
    if not gear:
        return jsonify({'message': 'Gear not found'}), 404
    return jsonify(gear.to_dict()), 200

@app.route('/gears/<int:id>', methods=['PUT'])
def update_gear(id):
    gear = Gears.query.get(id)
    if not gear:
        return jsonify({'message': 'Gear not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(gear, key, value)
    db.session.commit()
    return jsonify(gear.to_dict()), 200

@app.route('/gears/<int:id>', methods=['DELETE'])
def delete_gear(id):
    gear = Gears.query.get(id)
    if not gear:
        return jsonify({'message': 'Gear not found'}), 404
    db.session.delete(gear)
    db.session.commit()
    return jsonify({'message': 'Gear deleted successfully'}), 200

# Handlebars Routes
@app.route('/handlebars', methods=['GET'])
def get_handlebars():
    handlebars = Handlebars.query.all()
    return jsonify([handlebar.to_dict() for handlebar in handlebars]), 200

@app.route('/handlebars', methods=['POST'])
def create_handlebar():
    data = request.get_json()
    new_handlebar = Handlebars(**data)
    db.session.add(new_handlebar)
    db.session.commit()
    return jsonify(new_handlebar.to_dict()), 201

@app.route('/handlebars/<int:id>', methods=['GET'])
def get_handlebar(id):
    handlebar = Handlebars.query.get(id)
    if not handlebar:
        return jsonify({'message': 'Handlebar not found'}), 404
    return jsonify(handlebar.to_dict()), 200

@app.route('/handlebars/<int:id>', methods=['PUT'])
def update_handlebar(id):
    handlebar = Handlebars.query.get(id)
    if not handlebar:
        return jsonify({'message': 'Handlebar not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(handlebar, key, value)
    db.session.commit()
    return jsonify(handlebar.to_dict()), 200

@app.route('/handlebars/<int:id>', methods=['DELETE'])
def delete_handlebar(id):
    handlebar = Handlebars.query.get(id)
    if not handlebar:
        return jsonify({'message': 'Handlebar not found'}), 404
    db.session.delete(handlebar)
    db.session.commit()
    return jsonify({'message': 'Handlebar deleted successfully'}), 200

# Saddles Routes
@app.route('/saddles', methods=['GET'])
def get_saddles():
    saddles = Saddle.query.all()
    return jsonify([saddle.to_dict() for saddle in saddles]), 200

@app.route('/saddles', methods=['POST'])
def create_saddle():
    data = request.get_json()
    new_saddle = Saddle(**data)
    db.session.add(new_saddle)
    db.session.commit()
    return jsonify(new_saddle.to_dict()), 201

@app.route('/saddles/<int:id>', methods=['GET'])
def get_saddle(id):
    saddle = Saddle.query.get(id)
    if not saddle:
        return jsonify({'message': 'Saddle not found'}), 404
    return jsonify(saddle.to_dict()), 200

@app.route('/saddles/<int:id>', methods=['PUT'])
def update_saddle(id):
    saddle = Saddle.query.get(id)
    if not saddle:
        return jsonify({'message': 'Saddle not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(saddle, key, value)
    db.session.commit()
    return jsonify(saddle.to_dict()), 200

@app.route('/saddles/<int:id>', methods=['DELETE'])
def delete_saddle(id):
    saddle = Saddle.query.get(id)
    if not saddle:
        return jsonify({'message': 'Saddle not found'}), 404
    db.session.delete(saddle)
    db.session.commit()
    return jsonify({'message': 'Saddle deleted successfully'}), 200

# Seatposts Routes
@app.route('/seatposts', methods=['GET'])
def get_seatposts():
    seatposts = Seatpost.query.all()
    return jsonify([seatpost.to_dict() for seatpost in seatposts]), 200

@app.route('/seatposts', methods=['POST'])
def create_seatpost():
    data = request.get_json()
    new_seatpost = Seatpost(**data)
    db.session.add(new_seatpost)
    db.session.commit()
    return jsonify(new_seatpost.to_dict()), 201

@app.route('/seatposts/<int:id>', methods=['GET'])
def get_seatpost(id):
    seatpost = Seatpost.query.get(id)
    if not seatpost:
        return jsonify({'message': 'Seatpost not found'}), 404
    return jsonify(seatpost.to_dict()), 200

@app.route('/seatposts/<int:id>', methods=['PUT'])
def update_seatpost(id):
    seatpost = Seatpost.query.get(id)
    if not seatpost:
        return jsonify({'message': 'Seatpost not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(seatpost, key, value)
    db.session.commit()
    return jsonify(seatpost.to_dict()), 200

@app.route('/seatposts/<int:id>', methods=['DELETE'])
def delete_seatpost(id):
    seatpost = Seatpost.query.get(id)
    if not seatpost:
        return jsonify({'message': 'Seatpost not found'}), 404
    db.session.delete(seatpost)
    db.session.commit()
    return jsonify({'message': 'Seatpost deleted successfully'}), 200

# BrakePads Routes
@app.route('/brakepads', methods=['GET'])
def get_brakepads():
    brakepads = BrakePad.query.all()
    return jsonify([brakepad.to_dict() for brakepad in brakepads]), 200

@app.route('/brakepads', methods=['POST'])
def create_brakepad():
    data = request.get_json()
    new_brakepad = BrakePad(**data)
    db.session.add(new_brakepad)
    db.session.commit()
    return jsonify(new_brakepad.to_dict()), 201

@app.route('/brakepads/<int:id>', methods=['GET'])
def get_brakepad(id):
    brakepad = BrakePad.query.get(id)
    if not brakepad:
        return jsonify({'message': 'BrakePad not found'}), 404
    return jsonify(brakepad.to_dict()), 200

@app.route('/brakepads/<int:id>', methods=['PUT'])
def update_brakepad(id):
    brakepad = BrakePad.query.get(id)
    if not brakepad:
        return jsonify({'message': 'BrakePad not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(brakepad, key, value)
    db.session.commit()
    return jsonify(brakepad.to_dict()), 200

@app.route('/brakepads/<int:id>', methods=['DELETE'])
def delete_brakepad(id):
    brakepad = BrakePad.query.get(id)
    if not brakepad:
        return jsonify({'message': 'BrakePad not found'}), 404
    db.session.delete(brakepad)
    db.session.commit()
    return jsonify({'message': 'BrakePad deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)