from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorite = db.relationship("Favorite", back_populates="user")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": "*******"
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="favorite")

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship("Character", back_populates="favorite")

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", back_populates="favorite")

    def __init__(self, user_id, character_id, planet_id):
        self.user_id = user_id
        self.character_id = character_id
        self.planet_id = planet_id

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250))
    species = db.Column(db.String(250))
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))

    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", back_populates="character")

    favorite = db.relationship("Favorite", back_populates="character")

    def __init__(self, name, birth_year, species, height, mass, gender, hair_color, skin_color, homeworld):
        self.name = name
        self.birth_year = birth_year
        self.species = species
        self.height = height
        self.mass = mass
        self.gender = gender
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.homeworld = homeworld

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "species": self.species,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    rotation_period = db.Column(db.String(250))
    orbital_period = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.String(250))
    climate = db.Column(db.String(250))

    favorite = db.relationship("Favorite", back_populates="planet")
    character = db.relationship("Character", back_populates="planet")

    def __init__(self, name, population, rotation_period, orbital_period, diameter, gravity, terrain, surface_water, climate):
        self.name = name
        self.population = population
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.diameter = diameter
        self.gravity = gravity
        self.terrain = terrain
        self.surface_water = surface_water
        self.climate = climate

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "climate": self.climate
        }    