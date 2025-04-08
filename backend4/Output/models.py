from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name
        }

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    length = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)
    sequel_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=True)
    prequel_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'length': self.length,
            'rating': self.rating,
            'director_id': self.director_id,
            'sequel_id': self.sequel_id,
            'prequel_id': self.prequel_id
        }

class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    rating = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)
    seasons_count = db.Column(db.Integer)
    episodes_per_season = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'rating': self.rating,
            'director_id': self.director_id,
            'seasons_count': self.seasons_count,
            'episodes_per_season': self.episodes_per_season
        }

class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class MovieActor(db.Model):
    __tablename__ = 'movie_actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

class SeriesActor(db.Model):
    __tablename__ = 'series_actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'series_id': self.series_id,
            'actor_id': self.actor_id
        }