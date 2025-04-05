from flask import Flask, request, jsonify
from models import db, Team, Player

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Football API is Running'})

@app.route('/teams', methods=['GET'])
def get_all_teams():
    teams = Team.query.all()
    return jsonify([team.to_dict() for team in teams])

@app.route('/teams/<int:id>', methods=['GET'])
def get_specific_team(id):
    team = Team.query.get(id)
    if team:
        return jsonify(team.to_dict())
    return jsonify({'message': 'Team not found'}), 404

@app.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    new_team = Team(name=data['name'], city=data['city'], country=data['country'], stadium=data['stadium'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify(new_team.to_dict()), 201

@app.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get(id)
    if team:
        data = request.get_json()
        team.name = data['name']
        team.city = data['city']
        team.country = data['country']
        team.stadium = data['stadium']
        db.session.commit()
        return jsonify(team.to_dict())
    return jsonify({'message': 'Team not found'}), 404

@app.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get(id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'})
    return jsonify({'message': 'Team not found'}), 404

@app.route('/players', methods=['GET'])
def get_all_players():
    players = Player.query.all()
    return jsonify([player.to_dict() for player in players])

@app.route('/players/<int:id>', methods=['GET'])
def get_specific_player(id):
    player = Player.query.get(id)
    if player:
        return jsonify(player.to_dict())
    return jsonify({'message': 'Player not found'}), 404

@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    new_player = Player(name=data['name'], position=data['position'], team_id=data['team_id'], country=data['country'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player.to_dict()), 201

@app.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get(id)
    if player:
        data = request.get_json()
        player.name = data['name']
        player.position = data['position']
        player.team_id = data['team_id']
        player.country = data['country']
        db.session.commit()
        return jsonify(player.to_dict())
    return jsonify({'message': 'Player not found'}), 404

@app.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully'})
    return jsonify({'message': 'Player not found'}), 404

@app.route('/teams/<int:team_id>/players', methods=['GET'])
def get_players_by_team(team_id):
    players = Player.query.filter_by(team_id=team_id).all()
    return jsonify([player.to_dict() for player in players])

@app.route('/players/country/<string:country>', methods=['GET'])
def get_players_by_country(country):
    players = Player.query.filter_by(country=country).all()
    return jsonify([player.to_dict() for player in players])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)