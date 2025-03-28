"""
app_template.py

This is a skeleton for a Flask+Flask-SQLAlchemy application.
Please fill in the placeholders for the routes and any additional logic needed.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# -- CREATE FLASK APP --
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -- IMPORT MODELS (once they exist in models_template) --
# from models_template import ExampleModel

# -- CREATE ALL TABLES --
@app.before_first_request
def create_tables():
    db.create_all()

"""
Below are placeholders for your endpoints.
We give you an example endpoint for reference:
"""

@app.route('/example', methods=['GET'])
def get_example():
    # Example logic; adapt or remove as needed
    return jsonify({"message": "Example endpoint works!"})

# {{TEAM_ENDPOINTS}}
# For example:
# @app.route('/teams', methods=['GET'])
# def get_teams():
#     pass

# {{PLAYER_ENDPOINTS}}
# For example:
# @app.route('/players', methods=['GET'])
# def get_players():
#     pass

# More routes can be added here...

if __name__ == '__main__':
    app.run(debug=True)
