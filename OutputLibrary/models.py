from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    borrowed_flag = db.Column(db.Boolean, nullable=False, default=False)
    loans = db.relationship(
    'Loan',
    back_populates='book',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "borrowed_flag": self.borrowed_flag
        }

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email_address = db.Column(db.String(255), nullable=False)
    membership_number = db.Column(db.String(50), unique=True, nullable=False)
    membership_expiry_date = db.Column(db.Date, nullable=False)
    loans = db.relationship(
    'Loan',
    back_populates='member',
    lazy=True,
    cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email_address": self.email_address,
            "membership_number": self.membership_number,
            "membership_expiry_date": self.membership_expiry_date
        }

class Loan(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    returned_flag = db.Column(db.Boolean, nullable=False, default=False)
    book = db.relationship(
        'Book',
        back_populates='loans',
        lazy=True
    )
    member = db.relationship(
        'Member',
        back_populates='loans',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date,
            "returned_flag": self.returned_flag
        }

