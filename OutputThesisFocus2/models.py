from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    supervisorassignments = db.relationship(
    'SupervisorAssignment',
    back_populates='user',
    lazy='select',
    cascade="all, delete-orphan"
    )
    meetingnotes = db.relationship(
    'MeetingNote',
    back_populates='user',
    lazy='select'
    )
    reminderperiods = db.relationship(
    'ReminderPeriod',
    back_populates='user',
    lazy='select',
    cascade="all, delete-orphan"
    )
    notificationsettings = db.relationship(
    'NotificationSettings',
    uselist=False,
    back_populates='user',
    lazy='select'
    )
    theses = db.relationship(
        'Thesis',
        back_populates='user',
        lazy='select',
        foreign_keys=[Thesis.user_id]
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "name": self.name
        }

class Thesis(db.Model):
    __tablename__ = "theses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum('Seminar','Bachelor','Master','PhD', name='thesis_type'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    student_name = db.Column(db.String(255), nullable=False)
    start_supervision_date = db.Column(db.Date)
    official_registration_date = db.Column(db.Date)
    submission_date = db.Column(db.Date)
    colloquium_date = db.Column(db.Date)
    grade = db.Column(db.String(10))
    second_examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    supervisorassignments = db.relationship(
    'SupervisorAssignment',
    back_populates='thesis',
    lazy='select',
    cascade="all, delete-orphan"
    )
    meetingnotes = db.relationship(
    'MeetingNote',
    back_populates='thesis',
    lazy='select',
    cascade="all, delete-orphan"
    )
    deadline = db.relationship(
    'Deadline',
    uselist=False,
    back_populates='thesis',
    lazy='select'
    )
    user = db.relationship(
        'User',
        back_populates='theses',
        lazy='select',
        foreign_keys=[user_id]
    )
    second_examiner = db.relationship(
        'User',
        foreign_keys=[second_examiner_id],
        lazy='select'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "student_name": self.student_name,
            "start_supervision_date": self.start_supervision_date,
            "official_registration_date": self.official_registration_date,
            "submission_date": self.submission_date,
            "colloquium_date": self.colloquium_date,
            "grade": self.grade,
            "second_examiner_id": self.second_examiner_id,
            "user_id": self.user_id
        }

class SupervisorAssignment(db.Model):
    __tablename__ = "supervisor_assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignment_date = db.Column(db.Date, nullable=False)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    thesis = db.relationship(
        'Thesis',
        back_populates='supervisorassignments',
        lazy=True
    )
    user = db.relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='supervisorassignments',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "assignment_date": self.assignment_date,
            "thesis_id": self.thesis_id,
            "user_id": self.user_id
        }

class MeetingNote(db.Model):
    __tablename__ = "meeting_notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    thesis = db.relationship(
        'Thesis',
        back_populates='meetingnotes',
        lazy=True
    )
    user = db.relationship(
        'User',
        back_populates='meetingnotes',
        lazy=True,
        foreign_keys=[author_id]
    )

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "content": self.content,
            "author_id": self.author_id,
            "thesis_id": self.thesis_id
        }

class NotificationSettings(db.Model):
    __tablename__ = "notification_settings"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    in_app_enabled = db.Column(db.Boolean, nullable=False, default=True)
    email_enabled = db.Column(db.Boolean, nullable=False, default=True)
    user = db.relationship(
    'User',
    uselist=False,
    back_populates='notificationsettings',
    lazy=True
    )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "in_app_enabled": self.in_app_enabled,
            "email_enabled": self.email_enabled
        }

class Deadline(db.Model):
    __tablename__ = "deadlines"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deadline_date = db.Column(db.Date, nullable=False)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), unique=True, nullable=False)
    thesis = db.relationship(
    'Thesis',
    uselist=False,
    back_populates='deadline',
    lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "deadline_date": self.deadline_date,
            "thesis_id": self.thesis_id
        }

class ReminderPeriod(db.Model):
    __tablename__ = "reminder_periods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    days_before_deadline = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        'User',
        back_populates='reminderperiods',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "days_before_deadline": self.days_before_deadline,
            "user_id": self.user_id
        }

