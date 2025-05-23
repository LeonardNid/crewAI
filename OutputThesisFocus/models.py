from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    supervisorassignments = db.relationship('SupervisorAssignment', back_populates='user', lazy='select', cascade='all, delete-orphan')
    meetingnotes = db.relationship('MeetingNote', back_populates='user', lazy='select', cascade='all, delete-orphan')
    notificationsettings = db.relationship('NotificationSettings', uselist=False, back_populates='user', lazy='select', cascade='all, delete-orphan')
    reminderperiods = db.relationship('ReminderPeriod', back_populates='user', lazy='select', cascade='all, delete-orphan')
    thesiss = db.relationship('Thesis', back_populates='user', lazy='select', cascade='all, delete-orphan')
    points = db.relationship('Point', back_populates='user', lazy='select')

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
    type = db.Column(db.Enum('Seminar', 'Bachelor', 'Master', 'PhD', name='thesis_type'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    student_name = db.Column(db.String(255), nullable=False)
    start_supervision_date = db.Column(db.Date, nullable=True)
    official_registration_date = db.Column(db.Date, nullable=True)
    submission_date = db.Column(db.Date, nullable=True)
    colloquium_date = db.Column(db.Date, nullable=True)
    grade = db.Column(db.String(10), nullable=True)
    second_examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    supervisorassignments = db.relationship('SupervisorAssignment', back_populates='thesis', lazy='select', cascade='all, delete-orphan')
    meetingnotes = db.relationship('MeetingNote', back_populates='thesis', lazy='select', cascade='all, delete-orphan')
    deadline = db.relationship('Deadline', uselist=False, back_populates='thesis', lazy='select')
    user = db.relationship('User', back_populates='thesiss', lazy='select')

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
            "second_examiner_id": self.second_examiner_id
        }

class SupervisorAssignment(db.Model):
    __tablename__ = "supervisor_assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignment_date = db.Column(db.Date, nullable=False)
    thesis = db.relationship('Thesis', back_populates='supervisorassignments', lazy='select')
    user = db.relationship('User', back_populates='supervisorassignments', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "thesis_id": self.thesis_id,
            "user_id": self.user_id,
            "assignment_date": self.assignment_date
        }

class MeetingNote(db.Model):
    __tablename__ = "meeting_notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    thesis = db.relationship('Thesis', back_populates='meetingnotes', lazy='select')
    user = db.relationship('User', back_populates='meetingnotes', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "content": self.content,
            "thesis_id": self.thesis_id,
            "author_id": self.author_id
        }

class NotificationSettings(db.Model):
    __tablename__ = "notification_settings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    in_app_enabled = db.Column(db.Boolean, nullable=False)
    email_enabled = db.Column(db.Boolean, nullable=False)
    user = db.relationship('User', uselist=False, back_populates='notificationsettings', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "in_app_enabled": self.in_app_enabled,
            "email_enabled": self.email_enabled
        }

class Deadline(db.Model):
    __tablename__ = "deadlines"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('theses.id'), unique=True, nullable=False)
    deadline_date = db.Column(db.Date, nullable=False)
    thesis = db.relationship(
    'Thesis',
    uselist=False,
    back_populates='deadline',
    lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "thesis_id": self.thesis_id,
            "deadline_date": self.deadline_date
        }

class ReminderPeriod(db.Model):
    __tablename__ = "reminder_periods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    days_before_deadline = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='reminderperiods', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "days_before_deadline": self.days_before_deadline
        }

class BillTask(db.Model):
    __tablename__ = "billtasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    thesis = db.relationship('Thesis', uselist=False, back_populates='deadline', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "task_name": self.task_name,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

class CalPolicy(db.Model):
    __tablename__ = "calpolicys"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    policy_name = db.Column(db.String(255), nullable=False)
    effective_date = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    user = db.relationship('User', back_populates='reminderperiods', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "policy_name": self.policy_name,
            "effective_date": self.effective_date,
            "expiration_date": self.expiration_date,
            "active": self.active
        }

class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "campaign_name": self.campaign_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget
        }

class DiscountDistribution(db.Model):
    __tablename__ = "discountdistributions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distribution_name = db.Column(db.String(255), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.Date, nullable=True)
    valid_to = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "distribution_name": self.distribution_name,
            "discount_percentage": self.discount_percentage,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to
        }

class DonorReward(db.Model):
    __tablename__ = "donorrewards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reward_type = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "reward_type": self.reward_type,
            "amount": self.amount
        }

class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_number = db.Column(db.String(255), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "amount_due": self.amount_due,
            "due_date": self.due_date
        }

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "job_title": self.job_title,
            "description": self.description
        }

class LifeStage(db.Model):
    __tablename__ = "lifestages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stage_name = db.Column(db.String(255), nullable=False)
    age_range_start = db.Column(db.Integer, nullable=True)
    age_range_end = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "stage_name": self.stage_name,
            "age_range_start": self.age_range_start,
            "age_range_end": self.age_range_end
        }

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notification_text = db.Column(db.Text, nullable=False)
    sent_date = db.Column(db.Date, nullable=True)
    read = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "notification_text": self.notification_text,
            "sent_date": self.sent_date,
            "read": self.read
        }

class PaymentHistory(db.Model):
    __tablename__ = "paymenthistories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "payment_date": self.payment_date,
            "amount": self.amount,
            "method": self.method
        }

class PaymentMethod(db.Model):
    __tablename__ = "paymentmethods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    method_name = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "method_name": self.method_name
        }

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(255), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date
        }

class Point(db.Model):
    __tablename__ = "points"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='points', lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "points": self.points
        }

class Quest(db.Model):
    __tablename__ = "quests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "quest_name": self.quest_name,
            "description": self.description
        }

class RedeemRequest(db.Model):
    __tablename__ = "redeemrequests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, nullable=False)
    points_redeemed = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "points_redeemed": self.points_redeemed
        }

class RewardHistory(db.Model):
    __tablename__ = "rewardhistories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reward_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    redeemed_date = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "reward_id": self.reward_id,
            "user_id": self.user_id,
            "redeemed_date": self.redeemed_date
        }

class Reward(db.Model):
    __tablename__ = "rewards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reward_name = db.Column(db.String(255), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "reward_name": self.reward_name,
            "points_required": self.points_required
        }

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(255), nullable=False)
    permissions = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "role_name": self.role_name,
            "permissions": self.permissions
        }

class SocialMedia(db.Model):
    __tablename__ = "socialmedias"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_name = db.Column(db.String(255), nullable=False)
    profile_url = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "platform_name": self.platform_name,
            "profile_url": self.profile_url
        }

