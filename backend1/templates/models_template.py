"""
models_template.py

This is a skeleton for SQLAlchemy models using Flask-SQLAlchemy (from app_template).
"""

from app_template import db

class ExampleModel(db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

# {{TEAM_MODEL}}
# class Team(db.Model):
#     __tablename__ = 'teams'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     ...
#     def serialize(self):
#         return {...}

# {{PLAYER_MODEL}}
# class Player(db.Model):
#     ...
