from flask import Flask, request, jsonify
from models import db, User, Director, Movie, Series, Actor, MovieActor, SeriesActor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')

def home():
    return jsonify({'message': 'Movies and Series API is Running'})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], email=data['email'], name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    user.username = data['username']
    user.password = data['password']
    user.email = data['email']
    user.name = data['name']
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies])

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404
    return jsonify(movie.to_dict())

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], description=data['description'], length=data['length'],
                      rating=data['rating'], director_id=data['director_id'], sequel_id=data.get('sequel_id'),
                      prequel_id=data.get('prequel_id'))
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.to_dict()), 201

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404
    data = request.get_json()
    movie.title = data['title']
    movie.description = data['description']
    movie.length = data['length']
    movie.rating = data['rating']
    movie.director_id = data['director_id']
    movie.sequel_id = data.get('sequel_id')
    movie.prequel_id = data.get('prequel_id')
    db.session.commit()
    return jsonify(movie.to_dict())

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully'})

@app.route('/series', methods=['GET'])
def get_series():
    series = Series.query.all()
    return jsonify([s.to_dict() for s in series])

@app.route('/series/<int:id>', methods=['GET'])
def get_series_by_id(id):
    series = Series.query.get(id)
    if not series:
        return jsonify({'message': 'Series not found'}), 404
    return jsonify(series.to_dict())

@app.route('/series', methods=['POST'])
def create_series():
    data = request.get_json()
    new_series = Series(title=data['title'], description=data['description'], rating=data['rating'],
                        director_id=data['director_id'], seasons_count=data['seasons_count'],
                        episodes_per_season=data['episodes_per_season'])
    db.session.add(new_series)
    db.session.commit()
    return jsonify(new_series.to_dict()), 201

@app.route('/series/<int:id>', methods=['PUT'])
def update_series(id):
    series = Series.query.get(id)
    if not series:
        return jsonify({'message': 'Series not found'}), 404
    data = request.get_json()
    series.title = data['title']
    series.description = data['description']
    series.rating = data['rating']
    series.director_id = data['director_id']
    series.seasons_count = data['seasons_count']
    series.episodes_per_season = data['episodes_per_season']
    db.session.commit()
    return jsonify(series.to_dict())

@app.route('/series/<int:id>', methods=['DELETE'])
def delete_series(id):
    series = Series.query.get(id)
    if not series:
        return jsonify({'message': 'Series not found'}), 404
    db.session.delete(series)
    db.session.commit()
    return jsonify({'message': 'Series deleted successfully'})

@app.route('/directors', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    return jsonify([director.to_dict() for director in directors])

@app.route('/directors/<int:id>', methods=['GET'])
def get_director(id):
    director = Director.query.get(id)
    if not director:
        return jsonify({'message': 'Director not found'}), 404
    return jsonify(director.to_dict())

@app.route('/directors', methods=['POST'])
def create_director():
    data = request.get_json()
    new_director = Director(name=data['name'])
    db.session.add(new_director)
    db.session.commit()
    return jsonify(new_director.to_dict()), 201

@app.route('/directors/<int:id>', methods=['PUT'])
def update_director(id):
    director = Director.query.get(id)
    if not director:
        return jsonify({'message': 'Director not found'}), 404
    data = request.get_json()
    director.name = data['name']
    db.session.commit()
    return jsonify(director.to_dict())

@app.route('/directors/<int:id>', methods=['DELETE'])
def delete_director(id):
    director = Director.query.get(id)
    if not director:
        return jsonify({'message': 'Director not found'}), 404
    db.session.delete(director)
    db.session.commit()
    return jsonify({'message': 'Director deleted successfully'})

@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([actor.to_dict() for actor in actors])

@app.route('/actors/<int:id>', methods=['GET'])
def get_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        return jsonify({'message': 'Actor not found'}), 404
    return jsonify(actor.to_dict())

@app.route('/actors', methods=['POST'])
def create_actor():
    data = request.get_json()
    new_actor = Actor(name=data['name'])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify(new_actor.to_dict()), 201

@app.route('/actors/<int:id>', methods=['PUT'])
def update_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        return jsonify({'message': 'Actor not found'}), 404
    data = request.get_json()
    actor.name = data['name']
    db.session.commit()
    return jsonify(actor.to_dict())

@app.route('/actors/<int:id>', methods=['DELETE'])
def delete_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        return jsonify({'message': 'Actor not found'}), 404
    db.session.delete(actor)
    db.session.commit()
    return jsonify({'message': 'Actor deleted successfully'})

@app.route('/movies/<int:movie_id>/actors', methods=['POST'])
def add_actor_to_movie(movie_id):
    data = request.get_json()
    new_association = MovieActor(movie_id=movie_id, actor_id=data['actor_id'])
    db.session.add(new_association)
    db.session.commit()
    return jsonify({'message': 'Actor associated with movie successfully'}), 201

@app.route('/series/<int:series_id>/actors', methods=['POST'])
def add_actor_to_series(series_id):
    data = request.get_json()
    new_association = SeriesActor(series_id=series_id, actor_id=data['actor_id'])
    db.session.add(new_association)
    db.session.commit()
    return jsonify({'message': 'Actor associated with series successfully'}), 201

@app.route('/movies/<int:movie_id>/actors', methods=['GET'])
def get_actors_for_movie(movie_id):
    movie_actors = MovieActor.query.filter_by(movie_id=movie_id).all()
    actors = [Actor.query.get(actor_actor.actor_id).to_dict() for actor_actor in movie_actors]
    return jsonify(actors)

@app.route('/series/<int:series_id>/actors', methods=['GET'])
def get_actors_for_series(series_id):
    series_actors = SeriesActor.query.filter_by(series_id=series_id).all()
    actors = [Actor.query.get(actor_actor.actor_id).to_dict() for actor_actor in series_actors]
    return jsonify(actors)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)