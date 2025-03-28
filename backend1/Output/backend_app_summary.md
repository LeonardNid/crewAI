To create a system that models Teams and Players with CRUD operations using Flask, follow these steps:

1. **Define the Database Models**:
   - Create two classes `Team` and `Player` in your application.
   - Use SQLAlchemy for database integration.

```python
from flask import jsonify
from sqlalchemy import Column, Integer, String, ForeignKey

class Team(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    founded = Column(Integer)

class Player(db.Model):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(50))
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
```

2. **Set Up Flask Application and Routes**:
   - Initialize your Flask app.
   - Use `flask_restful` to create RESTful routes for Teams and Players.

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
api = Api(app)

class TeamResource(Resource):
    def get(self, id=None):
        try:
            if id is not None:
                team = Team.query.get(id)
                if team is None:
                    return {'message': 'Team not found'}, 404
                return jsonify(team.to_dict())
            teams = Team.query.all()
            return jsonify([team.to_dict() for team in teams])
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            new_team = Team(name=data['name'], founded=data['founded'])
            db.session.add(new_team)
            db.session.commit()
            return jsonify(new_team.to_dict()), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    def put(self, id):
        try:
            team = Team.query.get(id)
            if team is None:
                return {'message': 'Team not found'}, 404
            data = request.get_json()
            team.name = data['name']
            team.founded = data['founded']
            db.session.commit()
            return jsonify(team.to_dict())
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            team = Team.query.get(id)
            if team is None:
                return {'message': 'Team not found'}, 404
            db.session.delete(team)
            db.session.commit()
            return jsonify({'message': 'Team deleted successfully'})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

class PlayerResource(Resource):
    def get(self, id=None):
        try:
            if id is not None:
                player = Player.query.get(id)
                if player is None:
                    return {'message': 'Player not found'}, 404
                return jsonify(player.to_dict())
            players = Player.query.all()
            return jsonify([player.to_dict() for player in players])
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            new_player = Player(name=data['name'], position=data['position'], team_id=data['team_id'])
            db.session.add(new_player)
            db.session.commit()
            return jsonify(new_player.to_dict()), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    def put(self, id):
        try:
            player = Player.query.get(id)
            if player is None:
                return {'message': 'Player not found'}, 404
            data = request.get_json()
            player.name = data['name']
            player.position = data['position']
            player.team_id = data['team_id']
            db.session.commit()
            return jsonify(player.to_dict())
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            player = Player.query.get(id)
            if player is None:
                return {'message': 'Player not found'}, 404
            db.session.delete(player)
            db.session.commit()
            return jsonify({'message': 'Player deleted successfully'})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

api.add_resource(TeamResource, '/teams', '/teams/<int:id>')
api.add_resource(PlayerResource, '/players', '/players/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

This code sets up a RESTful API where you can perform CRUD operations on both Teams and Players. The system includes proper error handling and uses SQLAlchemy for database interactions, making it robust and scalable.