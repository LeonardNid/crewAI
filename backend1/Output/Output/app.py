from flask import Flask, jsonify, request
from models import db, Team, Player


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')

def home():
    return jsonify({'message': 'Football App is Running'})


@app.route('/health')

def health_check():
    return jsonify({'status': 'ok', 'database': db.engine.url})


@app.route('/teams', methods=['GET'])

def get_teams():
    try:
        teams = Team.query.all()
        return jsonify([team.to_dict() for team in teams])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/teams', methods=['POST'])

def create_team():
    try:
        data = request.get_json()
        new_team = Team(name=data['name'], founded=data['founded'], stadium=data['stadium'])
        db.session.add(new_team)
        db.session.commit()
        return jsonify(new_team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/teams/<int:id>', methods=['GET'])

def get_team(id):
    try:
        team = Team.query.get(id)
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        return jsonify(team.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/teams/<int:id>', methods=['PUT'])

def update_team(id):
    try:
        team = Team.query.get(id)
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        data = request.get_json()
        team.name = data['name']
        team.founded = data['founded']
        db.session.commit()
        return jsonify(team.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/teams/<int:id>', methods=['DELETE'])

def delete_team(id):
    try:
        team = Team.query.get(id)
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/players', methods=['GET'])

def get_players():
    try:
        players = Player.query.all()
        return jsonify([player.to_dict() for player in players])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/players', methods=['POST'])

def create_player():
    try:
        data = request.get_json()
        new_player = Player(name=data['name'], position=data['position'], team_id=data['team_id'])
        db.session.add(new_player)
        db.session.commit()
        return jsonify(new_player.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/players/<int:id>', methods=['GET'])

def get_player(id):
    try:
        player = Player.query.get(id)
        if not player:
            return jsonify({'message': 'Player not found'}), 404
        return jsonify(player.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/players/<int:id>', methods=['PUT'])

def update_player(id):
    try:
        player = Player.query.get(id)
        if not player:
            return jsonify({'message': 'Player not found'}), 404
        data = request.get_json()
        player.name = data['name']
        player.position = data['position']
        player.team_id = data['team_id']
        db.session.commit()
        return jsonify(player.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/players/<int:id>', methods=['DELETE'])

def delete_player(id):
    try:
        player = Player.query.get(id)
        if not player:
            return jsonify({'message': 'Player not found'}), 404
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)