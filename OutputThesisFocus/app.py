from flask import Flask, request, jsonify
from models import db, User, Thesis, SupervisorAssignment, MeetingNote, NotificationSettings, Deadline, ReminderPeriod

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Thesis Management Extended with Missing Endpoints API running'})

# Create new user or list all users
@app.route('/users', methods=['GET', 'POST'])
def users(): 
    if request.method == 'GET':
        objs = User.query.all()
        return jsonify([o.to_dict(exclude_password=True) for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 400
        new_obj = User()
        new_obj.email = data.get('email')
        new_obj.name = data.get('name')
        new_obj.set_password(data.get('password'))
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict(exclude_password=True)), 201

# Authenticate user by email and password
@app.route('/users_login', methods=['POST'])
def users_login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify(user.to_dict(exclude_password=True))

# Retrieve or update notification settings for a specific user
@app.route('/users_<int:user_id>_notification_settings', methods=['GET', 'PUT'])
def users_int_user_id_notification_settings(user_id): 
    if request.method == 'GET':
        obj = NotificationSettings.query.filter_by(user_id=user_id).first()
        if not obj:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'NotificationSettings not found'}), 404
            # create default
            obj = NotificationSettings(user_id=user_id, in_app_enabled=True, email_enabled=True)
            db.session.add(obj)
            db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = NotificationSettings.query.filter_by(user_id=user_id).first()
        if not obj:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'NotificationSettings not found'}), 404
            obj = NotificationSettings(user_id=user_id)
            db.session.add(obj)
            db.session.commit()
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())

# List or create reminder periods for a specific user
@app.route('/users_<int:user_id>_reminder_periods', methods=['GET', 'POST'])
def users_int_user_id_reminder_periods(user_id): 
    if request.method == 'GET':
        objs = ReminderPeriod.query.filter_by(user_id=user_id).all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        user_id = user_id
        new_obj = ReminderPeriod(user_id=user_id, days_before_deadline=data.get('days_before_deadline'))
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Update or delete a specific reminder period for a specific user
@app.route('/users_<int:user_id>_reminder_periods_<int:id>', methods=['PUT', 'DELETE'])
def users_int_user_id_reminder_periods_int_id(user_id, id): 
    if request.method == 'PUT':
        obj = ReminderPeriod.query.filter_by(user_id=user_id, id=id).first()
        if not obj:
            return jsonify({"message": "ReminderPeriod not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = ReminderPeriod.query.filter_by(user_id=user_id, id=id).first()
        if not obj:
            return jsonify({"message": "ReminderPeriod not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "ReminderPeriod deleted"})

# List all theses or create a new thesis
@app.route('/theses', methods=['GET', 'POST'])
def theses(): 
    if request.method == 'GET':
        def normalize_type(t):
            if not t:
                return t
            type_map = {
                'seminar': 'Seminar',
                'bachelor': 'Bachelor',
                'master': 'Master',
                'master thesis': 'Master',
                'phd': 'PhD'
            }
            t_lower = t.lower()
            return type_map.get(t_lower, t)

        objs = Thesis.query.all()
        for o in objs:
            # Normalize types to prevent LookupError on serialization
            if hasattr(o, 'type') and o.type:
                o.type = normalize_type(o.type)
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        def normalize_type(t):
            if not t:
                return t
            type_map = {
                'seminar': 'Seminar',
                'bachelor': 'Bachelor',
                'master': 'Master',
                'master thesis': 'Master',
                'phd': 'PhD'
            }
            t_lower = t.lower()
            return type_map.get(t_lower, t)

        data = request.get_json()
        try:
            def parse_date(date_str):
                if date_str is None:
                    return None
                return datetime.strptime(date_str, '%Y-%m-%d').date()

            data['start_supervision_date'] = parse_date(data.get('start_supervision_date'))
            data['official_registration_date'] = parse_date(data.get('official_registration_date'))
            data['submission_date'] = parse_date(data.get('submission_date'))
            data['colloquium_date'] = parse_date(data.get('colloquium_date'))
        except Exception as e:
            return jsonify({'message': 'Invalid date format'}), 400

        if 'type' in data:
            data['type'] = normalize_type(data['type'])

        new_obj = Thesis(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Filter theses by thesis type
@app.route('/theses_type_<string:type>', methods=['GET'])
def theses_type_string_type(type):
    def normalize_type(t):
        if not t:
            return t
        type_map = {
            'seminar': 'Seminar',
            'bachelor': 'Bachelor',
            'master': 'Master',
            'master thesis': 'Master',
            'phd': 'PhD'
        }
        t_lower = t.lower()
        return type_map.get(t_lower, t)

    norm_type = normalize_type(type)
    objs = Thesis.query.filter_by(type=norm_type).all()
    return jsonify([o.to_dict() for o in objs])

# Filter theses by thesis grade
@app.route('/theses_grade_<string:grade>', methods=['GET'])
def theses_grade_string_grade(grade):
    objs = Thesis.query.filter_by(grade=grade).all()
    return jsonify([o.to_dict() for o in objs])

# Filter theses by second examiner user ID
@app.route('/theses_second_examiner_<int:user_id>', methods=['GET'])
def theses_second_examiner_int_user_id(user_id):
    objs = Thesis.query.filter_by(second_examiner_id=user_id).all()
    return jsonify([o.to_dict() for o in objs])

# Filter theses by supervisor user ID via SupervisorAssignment relationship
@app.route('/theses_supervisor_<int:user_id>', methods=['GET'])
def theses_supervisor_int_user_id(user_id):
    assignments = SupervisorAssignment.query.filter_by(user_id=user_id).all()
    thesis_ids = [a.thesis_id for a in assignments]
    objs = Thesis.query.filter(Thesis.id.in_(thesis_ids)).all()
    return jsonify([o.to_dict() for o in objs])

# Filter theses with deadlines within specified days
@app.route('/theses_deadline_proximity_<int:days>', methods=['GET'])
def theses_deadline_proximity_int_days(days):
    from datetime import datetime, timedelta
    import json
    threshold_date = (datetime.utcnow() + timedelta(days=days)).date()
    objs = Thesis.query.filter(Thesis.submission_date <= threshold_date).all()
    return jsonify([o.to_dict() for o in objs])

# Retrieve, update, or delete a specific thesis by ID; delete cascades supervisors, meeting notes, and deadline
@app.route('/theses_<int:id>', methods=['GET', 'PUT', 'DELETE'])
def theses_int_id(id): 
    if request.method == 'GET':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({"message": "Thesis not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        def normalize_type(t):
            if not t:
                return t
            type_map = {
                'seminar': 'Seminar',
                'bachelor': 'Bachelor',
                'master': 'Master',
                'master thesis': 'Master',
                'phd': 'PhD'
            }
            t_lower = t.lower()
            return type_map.get(t_lower, t)

        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({'message': 'Thesis not found'}), 404
        json_data = request.get_json()
        if 'type' in json_data:
            json_data['type'] = normalize_type(json_data['type'])
        for k, v in json_data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Thesis.query.get(id)
        if not obj:
            return jsonify({'message': 'Thesis not found'}), 404
        try:
            db.session.delete(obj)
            db.session.commit()
        except Exception:
            return jsonify({'message': 'Error deleting thesis'}), 500
        return jsonify({'message': 'Thesis deleted'})

# List supervisor assignments, add one or multiple supervisors, or replace all supervisors of a thesis
@app.route('/theses_<int:thesis_id>_supervisors', methods=['GET', 'POST', 'PUT'])
def theses_int_thesis_id_supervisors(thesis_id): 
    if request.method == 'GET':
        objs = SupervisorAssignment.query.filter_by(thesis_id=thesis_id).all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        objs = []
        for assignment_data in data.get('assignments', []):
            try:
                assignment_date_str = assignment_data.get('assignment_date')
                assignment_data['assignment_date'] = datetime.strptime(assignment_date_str, '%Y-%m-%d').date() if assignment_date_str else None
            except Exception:
                return jsonify({'message': 'Invalid date format for assignment_date'}), 400
            new_obj = SupervisorAssignment(thesis_id=thesis_id, **assignment_data)
            db.session.add(new_obj)
            objs.append(new_obj)
        db.session.commit()
        return jsonify([o.to_dict() for o in objs]), 201
    elif request.method == 'PUT':
        from datetime import datetime
        objs = SupervisorAssignment.query.filter_by(thesis_id=thesis_id).all()
        for obj in objs:
            db.session.delete(obj)
        new_assignments = request.get_json().get('assignments', [])
        new_objs = []
        for assignment_data in new_assignments:
            try:
                assignment_date_str = assignment_data.get('assignment_date')
                assignment_data['assignment_date'] = datetime.strptime(assignment_date_str, '%Y-%m-%d').date() if assignment_date_str else None
            except Exception:
                return jsonify({'message': 'Invalid date format for assignment_date'}), 400
            new_obj = SupervisorAssignment(thesis_id=thesis_id, **assignment_data)
            db.session.add(new_obj)
            new_objs.append(new_obj)
        db.session.commit()
        return jsonify([o.to_dict() for o in new_objs])

# Remove a specific supervisor from a thesis by user ID
@app.route('/theses_<int:thesis_id>_supervisors_<int:user_id>', methods=['DELETE'])
def theses_int_thesis_id_supervisors_int_user_id(thesis_id, user_id):
    obj = SupervisorAssignment.query.filter_by(thesis_id=thesis_id, user_id=user_id).first()
    if not obj:
        return jsonify({'message': 'SupervisorAssignment not found'}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({'message': 'SupervisorAssignment deleted'})

# List or create meeting notes for a specific thesis
@app.route('/theses_<int:thesis_id>_meeting_notes', methods=['GET', 'POST'])
def theses_int_thesis_id_meeting_notes(thesis_id): 
    if request.method == 'GET':
        objs = MeetingNote.query.filter_by(thesis_id=thesis_id).all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        try:
            date_str = data.get('date')
            data['date'] = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format for date'}), 400

        # force thesis_id from route param
        new_obj = MeetingNote(thesis_id=thesis_id, **data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update, or delete a specific meeting note of a thesis
@app.route('/theses_<int:thesis_id>_meeting_notes_<int:id>', methods=['GET', 'PUT', 'DELETE'])
def theses_int_thesis_id_meeting_notes_int_id(thesis_id, id): 
    if request.method == 'GET':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=id).first()
        if not obj:
            return jsonify({'message': 'MeetingNote not found'}), 404
        from datetime import datetime
        data = request.get_json()
        try:
            date_str = data.get('date')
            data['date'] = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format for date'}), 400
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = MeetingNote.query.filter_by(thesis_id=thesis_id, id=id).first()
        if not obj:
            return jsonify({"message": "MeetingNote not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "MeetingNote deleted"})

# View, set, or update the deadline for a specific thesis
@app.route('/theses_<int:thesis_id>_deadline', methods=['GET', 'PUT'])
def theses_int_thesis_id_deadline(thesis_id): 
    if request.method == 'GET':
        obj = Deadline.query.filter_by(thesis_id=thesis_id).first()
        if not obj:
            return jsonify({'message': 'Deadline not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        from datetime import datetime
        obj = Deadline.query.filter_by(thesis_id=thesis_id).first()
        data = request.get_json()
        try:
            deadline_date_str = data.get('deadline_date')
            data['deadline_date'] = datetime.strptime(deadline_date_str, '%Y-%m-%d').date() if deadline_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format for deadline_date'}), 400
        if not obj:
            new_obj = Deadline(thesis_id=thesis_id, **data)
            db.session.add(new_obj)
            db.session.commit()
            return jsonify(new_obj.to_dict()), 201
        else:
            for k, v in data.items():
                setattr(obj, k, v)
            db.session.commit()
            return jsonify(obj.to_dict())

# Retrieve aggregated thesis overview dashboard with optional filtering and sorting
@app.route('/dashboard', methods=['GET'])
def dashboard():
    objs = Thesis.query.all()
    for o in objs:
        # Normalize type string for safe serialization
        if hasattr(o, 'type') and o.type:
            o.type = {
                'Seminar': 'Seminar',
                'Bachelor': 'Bachelor',
                'Master': 'Master',
                'PhD': 'PhD'
            }.get(o.type, o.type)
    return jsonify([o.to_dict() for o in objs])

# List all bill tasks or create a new bill task
@app.route('/billtasks', methods=['GET', 'POST'])
def billtasks(): 
    if request.method == 'GET':
        objs = BillTask.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        try:
            due_date_str = data.get('due_date')
            data['due_date'] = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format for due_date'}), 400

        new_obj = BillTask(
            task_name=data.get('task_name'),
            due_date=data.get('due_date'),
            priority=data.get('priority'),
            completed=data.get('completed', False)
        )
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Get, update, or delete a bill task by ID
@app.route('/billtasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def billtask_by_id(id): 
    if request.method == 'GET':
        obj = BillTask.query.get(id)
        if not obj:
            return jsonify({'message': 'BillTask not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = BillTask.query.get(id)
        if not obj:
            return jsonify({'message': 'BillTask not found'}), 404
        from datetime import datetime

        data = request.get_json()
        try:
            due_date_str = data.get('due_date')
            data['due_date'] = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format for due_date'}), 400
        for k,v in data.items():
            setattr(obj,k,v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = BillTask.query.get(id)
        if not obj:
            return jsonify({'message': 'BillTask not found'}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'message': 'BillTask deleted'})

# List or create calpolicys
@app.route('/calpolicys', methods=['GET', 'POST'])
def calpolicys(): 
    if request.method == 'GET':
        objs = CalPolicy.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        try:
            effective_date_str = data.get('effective_date')
            expiration_date_str = data.get('expiration_date')
            data['effective_date'] = datetime.strptime(effective_date_str, '%Y-%m-%d').date() if effective_date_str else None
            data['expiration_date'] = datetime.strptime(expiration_date_str, '%Y-%m-%d').date() if expiration_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        new_obj = CalPolicy(
            policy_name=data.get('policy_name'),
            effective_date=data.get('effective_date'),
            expiration_date=data.get('expiration_date'),
            active=data.get('active', True)
        )
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Get, update or delete calpolicy by ID
@app.route('/calpolicys/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def calpolicy_by_id(id): 
    if request.method == 'GET':
        obj = CalPolicy.query.get(id)
        if not obj:
            return jsonify({'message': 'CalPolicy not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = CalPolicy.query.get(id)
        if not obj:
            return jsonify({'message': 'CalPolicy not found'}), 404
        from datetime import datetime

        data = request.get_json()
        try:
            effective_date_str = data.get('effective_date')
            expiration_date_str = data.get('expiration_date')
            data['effective_date'] = datetime.strptime(effective_date_str, '%Y-%m-%d').date() if effective_date_str else None
            data['expiration_date'] = datetime.strptime(expiration_date_str, '%Y-%m-%d').date() if expiration_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        for k,v in data.items():
            setattr(obj,k,v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = CalPolicy.query.get(id)
        if not obj:
            return jsonify({'message': 'CalPolicy not found'}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'message': 'CalPolicy deleted'})

# List or create campaigns
@app.route('/campaigns', methods=['GET', 'POST'])
def campaigns(): 
    if request.method == 'GET':
        objs = Campaign.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        try:
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')
            data['start_date'] = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            data['end_date'] = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        new_obj = Campaign(
            campaign_name=data.get('campaign_name'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            budget=data.get('budget')
        )
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Get, update or delete campaign by ID
@app.route('/campaigns/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def campaign_by_id(id): 
    if request.method == 'GET':
        obj = Campaign.query.get(id)
        if not obj:
            return jsonify({'message': 'Campaign not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Campaign.query.get(id)
        if not obj:
            return jsonify({'message': 'Campaign not found'}), 404
        from datetime import datetime

        data = request.get_json()
        try:
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')
            data['start_date'] = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            data['end_date'] = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        for k,v in data.items():
            setattr(obj,k,v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Campaign.query.get(id)
        if not obj:
            return jsonify({'message': 'Campaign not found'}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'message': 'Campaign deleted'})

# List or create discount distributions
@app.route('/discountdistributions', methods=['GET', 'POST'])
def discountdistributions(): 
    if request.method == 'GET':
        objs = DiscountDistribution.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import datetime

        data = request.get_json()
        try:
            valid_from_str = data.get('valid_from')
            valid_to_str = data.get('valid_to')
            data['valid_from'] = datetime.strptime(valid_from_str, '%Y-%m-%d').date() if valid_from_str else None
            data['valid_to'] = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        new_obj = DiscountDistribution(
            distribution_name=data.get('distribution_name'),
            discount_percentage=data.get('discount_percentage'),
            valid_from=data.get('valid_from'),
            valid_to=data.get('valid_to')
        )
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Get, update or delete discountdistribution by ID
@app.route('/discountdistributions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def discountdistribution_by_id(id): 
    if request.method == 'GET':
        obj = DiscountDistribution.query.get(id)
        if not obj:
            return jsonify({'message': 'DiscountDistribution not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = DiscountDistribution.query.get(id)
        if not obj:
            return jsonify({'message': 'DiscountDistribution not found'}), 404
        from datetime import datetime
         data = request.get_json()
        try:
            valid_from_str = data.get('valid_from')
            valid_to_str = data.get('valid_to')
            data['valid_from'] = datetime.strptime(valid_from_str, '%Y-%m-%d').date() if valid_from_str else None
            data['valid_to'] = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None
        except Exception:
            return jsonify({'message': 'Invalid date format'}), 400
        for k,v in data.items():
            setattr(obj,k,v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = DiscountDistribution.query.get(id)
        if not obj:
            return jsonify({'message': 'DiscountDistribution not found'}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'message': 'DiscountDistribution deleted'})

# List or create donor rewards
@app.route('/donorrewards', methods=['GET', 'POST'])
def donorrewards(): 
    if request.method == 'GET':
        objs = DonorReward.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = DonorReward(
            reward_type=data.get('reward_type'),
            amount=data.get('amount')
        )
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Get, update or delete donorreward by ID
@app.route('/donorrewards/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def donorreward_by_id(id): 
    if request.method == 'GET':
        obj = DonorReward.query.get(id)
        if not obj:
            return jsonify({'message': 'DonorReward not found'}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = DonorReward.query.get(id)
        if not obj:
            return jsonify({'message': 'DonorReward not found'}), 404
        data = request.get_json()
        for k,v in data.items():
            setattr(obj,k,v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = DonorReward.query.get(id)
        if not obj:
            return jsonify({'message': 'DonorReward not found'}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'message': 'DonorReward deleted'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)