"""
app_template.py

This is a skeleton for a Flask+Flask-SQLAlchemy application.
Please fill in the placeholders for the routes and any additional logic needed.
"""

from flask import Flask, request, jsonify
from models import db, ExampleModel # Import your models here

# -- CREATE FLASK APP --
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')

def home():
    return jsonify({'message': 'Example App is Running'})


@app.route('/health')

def health_check():
    return jsonify({'status': 'ok', 'database': db.engine.url})


"""
Below are placeholders for your endpoints.
Logic may be modified for special needs.
We give you an example endpoint for every CRUD-Operation for reference:
"""

@app.route('/examples', methods=['GET'])
def get_examples():
    try:
        examples = ExampleModel.query.all()
        return jsonify([example.to_dict() for example in examples])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/examples', methods=['POST'])
def create_example():
    try:
        data = request.get_json()
        new_example = ExampleModel(name=data['name'], text=data['text'])
        db.session.add(new_example)
        db.session.commit()
        return jsonify(new_example.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    

@app.route('/examples/<int:id>', methods=['GET'])
def get_example(id):
    try:
        example = ExampleModel.query.get(id)
        if not example:
            return jsonify({'message': 'Example not found'}), 404
        return jsonify(example.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/examples/<int:id>', methods=['PUT'])
def update_example(id):
    try:
        example = ExampleModel.query.get(id)
        if not example:
            return jsonify({'message': 'Example not found'}), 404
        data = request.get_json()
        example.name = data['name']
        example.text = data['text']
        db.session.commit()
        return jsonify(example.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
    
@app.route('/examples/<int:id>', methods=['DELETE'])
def delete_example(id):
    try:
        example = ExampleModel.query.get(id)
        if not example:
            return jsonify({'message': 'Example not found'}), 404
        db.session.delete(example)
        db.session.commit()
        return jsonify({'message': 'Example deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

'''
More endpoints can be added below.
'''

if __name__ == '__main__':
    app.run(debug=True)
