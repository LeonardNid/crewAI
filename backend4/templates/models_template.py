
"""
models_template.py

This is a skeleton for SQLAlchemy models using Flask-SQLAlchemy (from app_template).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ExampleModel(db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    text = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'text': self.text
        }

'''
More Models may be added below
'''