from flask import Flask, request, jsonify
from models import db, Team, Player

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')

def home():
    return jsonify({'message': 'Football API is Running'})

@app.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    if not all(key in data for key in ('name', 'city', 'country', 'stadium')):
        return jsonify({'error': 'Bad Request, all fields are required'}), 400
    new_team = Team(name=data['name'], city=data['city'], country=data['country'], stadium=data['stadium'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify(new_team.to_dict()), 201

@app.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams]), 200

@app.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    team = Team.query.get(id)
    if team is None:
        return jsonify({'error': 'Not Found'}), 404
    return jsonify(team.to_dict()), 200

@app.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get(id)
    if team is None:
        return jsonify({'error': 'Not Found'}), 404
    data = request.get_json()
    if not any(data.get(key) for key in ('name', 'city', 'country', 'stadium')):
        return jsonify({'error': 'Bad Request, at least one field must be provided'}), 400
    team.name = data.get('name', team.name)
    team.city = data.get('city', team.city)
    team.country = data.get('country', team.country)
    team.stadium = data.get('stadium', team.stadium)
    db.session.commit()
    return jsonify(team.to_dict()), 200

@app.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get(id)
    if team is None:
        return jsonify({'error': 'Not Found'}), 404
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'No Content'}), 204

@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    if not all(key in data for key in ('name', 'position', 'country', 'team_id')):
        return jsonify({'error': 'Bad Request, all fields are required'}), 400
    new_player = Player(name=data['name'], position=data['position'], country=data['country'], team_id=data['team_id'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player.to_dict()), 201

@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([player.to_dict() for player in players]), 200

@app.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id)
    if player is None:
        return jsonify({'error': 'Not Found'}), 404
    return jsonify(player.to_dict()), 200

@app.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get(id)
    if player is None:
        return jsonify({'error': 'Not Found'}), 404
    data = request.get_json()
    if not any(data.get(key) for key in ('name', 'position', 'country', 'team_id')):
        return jsonify({'error': 'Bad Request, at least one field must be provided'}), 400
    player.name = data.get('name', player.name)
    player.position = data.get('position', player.position)
    player.country = data.get('country', player.country)
    player.team_id = data.get('team_id', player.team_id)
    db.session.commit()
    return jsonify(player.to_dict()), 200

@app.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if player is None:
        return jsonify({'error': 'Not Found'}), 404
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'No Content'}), 204

@app.route('/teams/<int:team_id>/players', methods=['GET'])
def get_players_by_team(team_id):
    team = Team.query.get(team_id)
    if team is None:
        return jsonify({'error': 'Not Found'}), 404
    players = Player.query.filter_by(team_id=team_id).all()
    return jsonify([player.to_dict() for player in players]), 200

@app.route('/players/country/<string:country>', methods=['GET'])
def get_players_by_country(country):
    players = Player.query.filter_by(country=country).all()
    if not players:
        return jsonify({'error': 'Not Found'}), 404
    return jsonify([player.to_dict() for player in players]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)