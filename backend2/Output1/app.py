from flask import Flask, jsonify, request
from models import Base, Team, Player
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('football.db')
Base.metadata.create_all(db)

@app.route('/teams', methods=['GET'])
def get_all_teams():
    teams = db.query(Team).all()
    return jsonify([{'id': team.id, 'name': team.name, 'founded': team.founded, 'league': team.league} for team in teams])

@app.route('/teams/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        abort(404)
    return jsonify({'id': team.id, 'name': team.name, 'founded': team.founded, 'league': team.league})

@app.route('/teams', methods=['POST'])
def create_team():
    data = request.json
    new_team = Team(name=data['name'], founded=data['founded'], league=data['league'])
    db.add(new_team)
    db.commit()
    return jsonify({'id': new_team.id}), 201

@app.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        abort(404)
    data = request.json
    team.name = data.get('name', team.name)
    team.founded = data.get('founded', team.founded)
    team.league = data.get('league', team.league)
    db.commit()
    return jsonify({'id': team.id, 'name': team.name, 'founded': team.founded, 'league': team.league})

@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        abort(404)
    db.delete(team)
    db.commit()
    return jsonify({'message': 'Team deleted successfully'})

@app.route('/players', methods=['GET'])
def get_all_players():
    players = db.query(Player).all()
    return jsonify([{'id': player.id, 'name': player.name, 'position': player.position, 'team_id': player.team_id} for player in players])

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        abort(404)
    return jsonify({'id': player.id, 'name': player.name, 'position': player.position, 'team_id': player.team_id})

@app.route('/players', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(name=data['name'], position=data['position'], team_id=data['team_id'])
    db.add(new_player)
    db.commit()
    return jsonify({'id': new_player.id}), 201

@app.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        abort(404)
    data = request.json
    player.name = data.get('name', player.name)
    player.position = data.get('position', player.position)
    player.team_id = data.get('team_id', player.team_id)
    db.commit()
    return jsonify({'id': player.id, 'name': player.name, 'position': player.position, 'team_id': player.team_id})

@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        abort(404)
    db.delete(player)
    db.commit()
    return jsonify({'message': 'Player deleted successfully'})