from flask import Flask, request, jsonify
from models import db, User, Thesis, SupervisorAssignment, MeetingNote, NotificationSettings, Deadline, ReminderPeriod

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Thesis Management API running'})

# Create a new user with email, password (plaintext, to be hashed internally), and name
@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()
    from werkzeug.security import generate_password_hash
    hashed_password = generate_password_hash(data.get('password'))
    data['password_hash'] = hashed_password
    # Remove plain password key to not cause error if constructor expects password_hash only
    data.pop('password', None)
    new_obj = User(**data)
    db.session.add(new_obj)
    db.session.commit()
    return jsonify(new_obj.to_dict()), 201

# Authenticate a user by email and password (login)
@app.route('/users/login', methods=['POST'])
def users_login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user is not None:
        from werkzeug.security import check_password_hash
        if check_password_hash(user.password_hash, data.get('password')):
            return jsonify(user.to_dict()), 200
    return jsonify({"message": "Authentication failed"}), 401

# Retrieve or update a user's notification settings
@app.route('/users/<int:id>/notification_settings', methods=['GET', 'PUT'])
def users_int_id_notification_settings(id): 
    if request.method == 'GET':
        parent = User.query.get(id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        children = parent.notificationsettings
        return jsonify([children.to_dict()] if children else [])
    elif request.method == 'PUT':
        parent = User.query.get(id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        data = request.get_json()
        notification_settings = parent.notificationsettings
        if notification_settings:
            for k, v in data.items():
                setattr(notification_settings, k, v)
            db.session.commit()
            return jsonify(notification_settings.to_dict())
        else:
            new_settings = NotificationSettings(user_id=id, **data)
            db.session.add(new_settings)
            db.session.commit()
            return jsonify(new_settings.to_dict()), 201

# List all reminder periods for a user or create a new reminder period
@app.route('/users/<int:id>/reminder_periods', methods=['GET', 'POST'])
def users_int_id_reminder_periods(id): 
    if request.method == 'GET':
        parent = User.query.get(id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        children = parent.reminderperiods
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        data['user_id'] = id
        new_obj = ReminderPeriod(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Update or delete an existing reminder period for a user
@app.route('/users/<int:id>/reminder_periods/<int:reminder_id>', methods=['PUT', 'DELETE'])
def users_int_id_reminder_periods_int_reminder_id(id, reminder_id): 
    if request.method == 'PUT':
        obj = ReminderPeriod.query.filter_by(user_id=id, id=reminder_id).first()
        if not obj:
            return jsonify({"message": "ReminderPeriod not found"}), 404
            
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = ReminderPeriod.query.filter_by(user_id=id, id=reminder_id).first()
        if not obj:
            return jsonify({"message": "ReminderPeriod not found"}), 404
            
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "ReminderPeriod deleted"})

# Delete a user and cascade delete related supervisor assignments and notification settings
@app.route('/users/<int:id>', methods=['DELETE'])
def users_int_id(id):
    obj = User.query.get(id)
    if not obj:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# List all theses or create a new thesis
@app.route('/theses', methods=['GET', 'POST'])
def theses(): 
    if request.method == 'GET':
        objs = Thesis.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Thesis(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Filter theses by thesis type
@app.route('/theses/type/<string:type>', methods=['GET'])
def theses_type_string_type(type):
    objs = Thesis.query.filter_by(type=type).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Filter theses by grade
@app.route('/theses/grade/<string:grade>', methods=['GET'])
def theses_grade_string_grade(grade):
    objs = Thesis.query.filter_by(grade=grade).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Filter theses by second examiner user ID
@app.route('/theses/second_examiner/<int:user_id>', methods=['GET'])
def theses_second_examiner_int_user_id(user_id):
    objs = Thesis.query.filter_by(second_examiner_id=user_id).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Filter theses by supervisor user ID via supervisor assignments
@app.route('/theses/supervisor/<int:user_id>', methods=['GET'])
def theses_supervisor_int_user_id(user_id):
    objs = db.session.query(Thesis).join(SupervisorAssignment).filter(SupervisorAssignment.user_id == user_id).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Filter theses by deadline proximity within given days
@app.route('/theses/deadline_proximity/<int:days>', methods=['GET'])
def theses_deadline_proximity_int_days(days):
    # 'deadline_proximity' filter is domain specific and must be implemented appropriately
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    threshold = now + timedelta(days=days)
    objs = Thesis.query.filter(Thesis.submission_date <= threshold.strftime('%Y-%m-%d')).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve, update, or delete a thesis by ID with cascading deletes of related entities
@app.route('/theses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def theses_int_id(id): 
    if request.method == 'GET':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({"message": "Thesis not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({"message": "Thesis not found"}), 404

        # Update thesis attributes
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({"message": "Thesis not found"}), 404
        # Assuming cascading delete configured in database schema or handled here explicitly
        SupervisorAssignment.query.filter_by(thesis_id=id).delete()
        MeetingNote.query.filter_by(thesis_id=id).delete()
        deadline = Deadline.query.filter_by(thesis_id=id).first()
        if deadline:
            db.session.delete(deadline)
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Thesis deleted"})

# List all supervisors assigned to a thesis, add supervisor, or replace all supervisors
@app.route('/theses/<int:id>/supervisors', methods=['GET', 'POST', 'PUT'])
def theses_int_id_supervisors(id): 
    if request.method == 'GET':
        parent = Thesis.query.get(id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        children = parent.supervisorassignments
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        data["thesis_id"] = id
        new_obj = SupervisorAssignment(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201
    elif request.method == 'PUT':
        parent = Thesis.query.get(id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        # Remove all existing supervisors
        SupervisorAssignment.query.filter_by(thesis_id=id).delete()
        # Add new supervisors
        new_supervisors = request.get_json()
        if not isinstance(new_supervisors, list):
            return jsonify({"message": "Invalid data format, expected a list"}), 400
        for supervisor_data in new_supervisors:
            supervisor_data["thesis_id"] = id
            new_obj = SupervisorAssignment(**supervisor_data)
            db.session.add(new_obj)
        db.session.commit()
        return jsonify({"message": "Supervisors replaced"})

# Remove a specific supervisor from a thesis by thesis ID and supervisor user ID
@app.route('/theses/<int:id>/supervisors/<int:user_id>', methods=['DELETE'])
def theses_int_id_supervisors_int_user_id(id, user_id):
    obj = SupervisorAssignment.query.filter_by(thesis_id=id, user_id=user_id).first()
    if not obj:
        return jsonify({"message": "SupervisorAssignment not found"}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"message": "SupervisorAssignment deleted"})

# List all meeting notes for a thesis or create a new meeting note
@app.route('/theses/<int:id>/meeting_notes', methods=['GET', 'POST'])
def theses_int_id_meeting_notes(id): 
    if request.method == 'GET':
        parent = Thesis.query.get(id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        children = parent.meetingnotes
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        data["thesis_id"] = id
        new_obj = MeetingNote(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update, or delete a specific meeting note by thesis ID and note ID
@app.route('/theses/<int:id>/meeting_notes/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def theses_int_id_meeting_notes_int_note_id(id, note_id): 
    if request.method == 'GET':
        obj = MeetingNote.query.filter_by(thesis_id=id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = MeetingNote.query.filter_by(thesis_id=id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = MeetingNote.query.filter_by(thesis_id=id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "MeetingNote deleted"})

# Retrieve or set/update the deadline for a thesis
@app.route('/theses/<int:id>/deadline', methods=['GET', 'PUT'])
def theses_int_id_deadline(id): 
    if request.method == 'GET':
        parent = Thesis.query.get(id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        deadline = parent.deadline
        return jsonify(deadline.to_dict() if deadline else {})
    elif request.method == 'PUT':
        parent = Thesis.query.get(id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        data = request.get_json()
        deadline = parent.deadline
        if not deadline:
            deadline = Deadline(thesis_id=id, **data)
            db.session.add(deadline)
        else:
            for k, v in data.items():
                setattr(deadline, k, v)
        db.session.commit()
        return jsonify(deadline.to_dict())

# Retrieve an aggregated thesis overview on the dashboard with optional filters and sorting
@app.route('/dashboard', methods=['GET'])
def dashboard():
    objs = Thesis.query.all()
    return jsonify([o.to_dict() for o in objs])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)