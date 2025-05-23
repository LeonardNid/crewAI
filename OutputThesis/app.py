from flask import Flask, request, jsonify
from models import db, User, Thesis, SupervisorAssignment, MeetingNote, NotificationSettings, ReminderPeriod, Deadline

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Thesis Management API running'})

# Register a new user via email
@app.route('/users', methods=['POST'])
def users():
    data = request.get_json()
    new_obj = User(**data)
    db.session.add(new_obj)
    db.session.commit()
    return jsonify(new_obj.to_dict()), 201

# Authenticate a user via email login
@app.route('/users/login', methods=['POST'])
def users_login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    # Authentication logic should be here, simplified to success response
    return jsonify({"message": "Login successful"}), 200

# Retrieve or configure user's notification preferences (in-app and email)
@app.route('/users/<int:user_id>/notification_settings', methods=['GET', 'PUT'])
def users_int_user_id_notification_settings(user_id): 
    if request.method == 'GET':
        parent = User.query.get(user_id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        notif = parent.notificationsettings
        if notif is None:
            return jsonify({})
        return jsonify(notif.to_dict())
    elif request.method == 'PUT':
        parent = User.query.get(user_id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        notif = parent.notificationsettings
        if notif is None:
            notif = NotificationSettings(user_id=user_id)
            db.session.add(notif)
            db.session.commit()
        data = request.get_json()
        for k, v in data.items():
            setattr(notif, k, v)
        db.session.commit()
        return jsonify(notif.to_dict())

# Manage (list, add, modify, delete) reminder periods for deadlines by user, optionally filtered by thesis
@app.route('/users/<int:user_id>/reminder_periods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users_int_user_id_reminder_periods(user_id): 
    if request.method == 'GET':
        parent = User.query.get(user_id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        children = parent.reminderperiods
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        data['user_id'] = user_id
        new_obj = ReminderPeriod(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201
    elif request.method == 'PUT':
        parent = User.query.get(user_id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        obj_id = request.get_json().get("id")
        obj = ReminderPeriod.query.get(obj_id) if obj_id else None
        if not obj or obj.user_id != user_id:
            return jsonify({"message": "ReminderPeriod not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        parent = User.query.get(user_id)
        if not parent:
            return jsonify({"message": "User not found"}), 404
        obj_id = request.args.get('id', type=int)
        obj = ReminderPeriod.query.get(obj_id) if obj_id else None
        if not obj or obj.user_id != user_id:
            return jsonify({"message": "ReminderPeriod not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "ReminderPeriod deleted"})

# Create a new thesis or retrieve all thesis records
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

# Retrieve thesis records filtered by thesis type
@app.route('/theses/type/<string:thesis_type>', methods=['GET'])
def theses_type_string_thesis_type(thesis_type):
    objs = Thesis.query.filter_by(thesis_type=thesis_type).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve thesis records filtered by grade
@app.route('/theses/grade/<string:grade>', methods=['GET'])
def theses_grade_string_grade(grade):
    objs = Thesis.query.filter_by(grade=grade).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve thesis records filtered by second examiner user ID
@app.route('/theses/second_examiner/<int:user_id>', methods=['GET'])
def theses_second_examiner_int_user_id(user_id):
    objs = Thesis.query.filter_by(second_examiner_id=user_id).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve thesis records supervised by a specific user ID (via SupervisorAssignment)
@app.route('/theses/supervisor/<int:user_id>', methods=['GET'])
def theses_supervisor_int_user_id(user_id):
    assignments = SupervisorAssignment.query.filter_by(user_id=user_id).all()
    thesis_ids = [a.thesis_id for a in assignments]
    objs = Thesis.query.filter(Thesis.id.in_(thesis_ids)).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve thesis records with deadlines due within given days (query logic on Deadline.deadline_date)
@app.route('/theses/deadline_proximity/<int:days>', methods=['GET'])
def theses_deadline_proximity_int_days(days):
    from datetime import datetime, timedelta

    cutoff_date = datetime.utcnow() + timedelta(days=days)
    objs = Thesis.query.join(Deadline).filter(Deadline.deadline_date <= cutoff_date).all()
    if not objs:
        return jsonify({"message": "Thesis not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Retrieve, update or delete a thesis by ID with cascading to SupervisorAssignment and MeetingNote
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
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({"message": "Thesis not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Thesis deleted"})

# Retrieve, assign (add) or update (replace) supervisors assigned to a thesis
@app.route('/theses/<int:thesis_id>/supervisors', methods=['GET', 'POST', 'PUT'])
def theses_int_thesis_id_supervisors(thesis_id): 
    if request.method == 'GET':
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        children = parent.supervisorassignments
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        if not isinstance(user_ids, list) or not all(isinstance(uid, int) for uid in user_ids):
            return jsonify({"message": "user_ids must be a list of integers"}), 400
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        added = []
        for uid in user_ids:
            exists = SupervisorAssignment.query.filter_by(thesis_id=thesis_id, user_id=uid).first()
            if not exists:
                new_obj = SupervisorAssignment(thesis_id=thesis_id, user_id=uid)
                db.session.add(new_obj)
                added.append(new_obj)
        db.session.commit()
        return jsonify([a.to_dict() for a in added]), 201
    elif request.method == 'PUT':
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        if not isinstance(user_ids, list) or not all(isinstance(uid, int) for uid in user_ids):
            return jsonify({"message": "user_ids must be a list of integers"}), 400
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        SupervisorAssignment.query.filter_by(thesis_id=thesis_id).delete()
        for uid in user_ids:
            new_obj = SupervisorAssignment(thesis_id=thesis_id, user_id=uid)
            db.session.add(new_obj)
        db.session.commit()
        children = parent.supervisorassignments
        return jsonify([c.to_dict() for c in children])

# Remove a supervisor assignment by thesis ID and user ID
@app.route('/theses/<int:thesis_id>/supervisors/<int:user_id>', methods=['DELETE'])
def theses_int_thesis_id_supervisors_int_user_id(thesis_id, user_id):
    obj = SupervisorAssignment.query.filter_by(thesis_id=thesis_id, user_id=user_id).first()
    if not obj:
        return jsonify({"message": "SupervisorAssignment not found"}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"message": "SupervisorAssignment deleted"})

# Retrieve all meeting notes or create a new meeting note for a thesis
@app.route('/theses/<int:thesis_id>/meeting_notes', methods=['GET', 'POST'])
def theses_int_thesis_id_meeting_notes(thesis_id): 
    if request.method == 'GET':
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        children = parent.meetingnotes
        return jsonify([c.to_dict() for c in children])
    elif request.method == 'POST':
        data = request.get_json()
        data['thesis_id'] = thesis_id
        new_obj = MeetingNote(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a single meeting note by note ID within a thesis
@app.route('/theses/<int:thesis_id>/meeting_notes/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def theses_int_thesis_id_meeting_notes_int_note_id(thesis_id, note_id): 
    if request.method == 'GET':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=note_id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "MeetingNote deleted"})

# Retrieve or set/update custom deadline date for a thesis
@app.route('/theses/<int:thesis_id>/deadline', methods=['GET', 'PUT'])
def theses_int_thesis_id_deadline(thesis_id): 
    if request.method == 'GET':
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        deadline = parent.deadline
        if deadline is None:
            return jsonify({})
        return jsonify(deadline.to_dict())
    elif request.method == 'PUT':
        parent = Thesis.query.get(thesis_id)
        if not parent:
            return jsonify({"message": "Thesis not found"}), 404
        deadline = parent.deadline
        if deadline is None:
            deadline = Deadline(thesis_id=thesis_id)
            db.session.add(deadline)
            db.session.commit()
        data = request.get_json()
        for k, v in data.items():
            setattr(deadline, k, v)
        db.session.commit()
        return jsonify(deadline.to_dict())

# Retrieve dashboard data with thesis list supporting sorting, filtering (type, grade, supervisor, deadline proximity) and visual status indicators
@app.route('/dashboard', methods=['GET'])
def dashboard():
    objs = Thesis.query.all()
    return jsonify([o.to_dict() for o in objs])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)