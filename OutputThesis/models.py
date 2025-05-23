from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    supervisorassignments = db.relationship(
    'SupervisorAssignment',
    back_populates='user',
    lazy=True,
    cascade="all, delete-orphan"
    )
    thesiss = db.relationship(
    'Thesis',
    back_populates='user',
    lazy=True,

    )
    meetingnotes = db.relationship(
    'MeetingNote',
    back_populates='user',
    lazy=True,

    )
    notificationsettings = db.relationship(
    'NotificationSettings',
    uselist=False,
    back_populates='user',
    lazy=True
    )
    reminderperiods = db.relationship(
    'ReminderPeriod',
    back_populates='user',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name
        }

class Thesis(db.Model):
    __tablename__ = "theses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thesis_type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    student_name = db.Column(db.String(255), nullable=False)
    start_supervision_date = db.Column(db.Date)
    official_registration_date = db.Column(db.Date)
    submission_date = db.Column(db.Date)
    colloquium_date = db.Column(db.Date)
    grade = db.Column(db.String(10))
    second_examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    supervisorassignments = db.relationship(
    'SupervisorAssignment',
    back_populates='thesis',
    lazy=True,
    cascade="all, delete-orphan"
    )
    meetingnotes = db.relationship(
    'MeetingNote',
    back_populates='thesis',
    lazy=True,
    cascade="all, delete-orphan"
    )
    user = db.relationship(
        'User',
        back_populates='thesiss',
        lazy=True
    )
    deadline = db.relationship(
    'Deadline',
    uselist=False,
    back_populates='thesis',
    lazy=True
    )
    reminderperiods = db.relationship(
    'ReminderPeriod',
    back_populates='thesis',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "thesis_type": self.thesis_type,
            "title": self.title,
            "description": self.description,
            "student_name": self.student_name,
            "start_supervision_date": self.start_supervision_date,
            "official_registration_date": self.official_registration_date,
            "submission_date": self.submission_date,
            "colloquium_date": self.colloquium_date,
            "grade": self.grade,
            "second_examiner_id": self.second_examiner_id
        }

class SupervisorAssignment(db.Model):
    __tablename__ = "supervisor_assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    assigned_date = db.Column(db.Date)
    user = db.relationship(
        'User',
        back_populates='supervisorassignments',
        lazy=True
    )
    thesis = db.relationship(
        'Thesis',
        back_populates='supervisorassignments',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "thesis_id": self.thesis_id,
            "assigned_date": self.assigned_date
        }

class MeetingNote(db.Model):
    __tablename__ = "meeting_notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    date = db.Column(db.Date)
    summary = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    thesis = db.relationship(
        'Thesis',
        back_populates='meetingnotes',
        lazy=True
    )
    user = db.relationship(
        'User',
        back_populates='meetingnotes',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "thesis_id": self.thesis_id,
            "date": self.date,
            "summary": self.summary,
            "creator_id": self.creator_id
        }

class NotificationSettings(db.Model):
    __tablename__ = "notification_settings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    in_app_enabled = db.Column(db.Boolean, default=True)
    email_enabled = db.Column(db.Boolean, default=True)
    user = db.relationship(
    'User',
    uselist=False,
    back_populates='notificationsettings',
    lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "in_app_enabled": self.in_app_enabled,
            "email_enabled": self.email_enabled
        }

class ReminderPeriod(db.Model):
    __tablename__ = "reminder_periods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=True)
    days_before_deadline = db.Column(db.Integer, nullable=False)
    user = db.relationship(
        'User',
        back_populates='reminderperiods',
        lazy=True
    )
    thesis = db.relationship(
        'Thesis',
        back_populates='reminderperiods',
        lazy=True
    )
    deadline = db.relationship(
        'Deadline',
        back_populates='reminderperiods',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "thesis_id": self.thesis_id,
            "days_before_deadline": self.days_before_deadline
        }

class Deadline(db.Model):
    __tablename__ = "deadlines"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), unique=True, nullable=False)
    deadline_date = db.Column(db.Date)
    thesis = db.relationship(
    'Thesis',
    uselist=False,
    back_populates='deadline',
    lazy=True
    )
    reminderperiods = db.relationship(
    'ReminderPeriod',
    back_populates='deadline',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "thesis_id": self.thesis_id,
            "deadline_date": self.deadline_date
        }

