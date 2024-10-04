from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False) 
    lastname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorite_character = db.relationship("Favorite_Character", backref="user", lazy=True)
    favorite_planet = db.relationship("Favorite_Planet", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    homeplanet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    homeplanet = db.relationship("Planets", backref='characters', lazy=True)
    favorite_character = db.relationship("Favorite_Character", backref="characters", lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "height": self.height,
            "gender": self.gender,
            "homeplanet_name": self.homeplanet.name if self.homeplanet else None,
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(40), nullable=False)
    population = db.Column(db.String(40), nullable=False, unique=True)
    gravity = db.Column(db.String(40), nullable=False)
    favorite_planet = db.relationship("Favorite_Planet", backref="planets", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "population": self.population,
            "gravity": self.gravity
        }

class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return '<FavoriteCharacter user_id=%r, character_id=%r>' % (self.user_id, self.character_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))

    def __repr__(self):
        return '<FavoritePlanet user_id=%r, planet_id=%r>' % (self.user_id, self.planet_id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }