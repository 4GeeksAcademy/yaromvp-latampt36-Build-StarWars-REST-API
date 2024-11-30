"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#   +++ USERS +++
@app.route("/users", methods=["POST"])
def sign_up():
	data = request.json
	email = data.get("email")
	password = data.get("password")
	if None in (email, password):
		return jsonify({
			"message": "Email and Password required"
		}), 400
	user_already_exist = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
	if user_already_exist:
		return jsonify({
			"message": "Unable to create the user"
		}), 400
	new_user = User(email, password)
	if not isinstance(new_user, User):
		return jsonify ({
			"message": "Server error... Try again later"
		})
	try:
		db.session.add(new_user)
		db.session.commit()
	except:
		return jsonify({
			"message": "Database error"
		}), 500
	user_serialized = new_user.serialize()
	return jsonify(user_serialized), 201

@app.route("/users", methods=["GET"])
def get_users():
	users_result = db.session.execute(db.select(User)).all()
	users = []
	for user_tuple in users_result:
		users.append(user_tuple[0])
	users_serialized = []
	for user in users:
		users_serialized.append(user.serialize())
	return jsonify(users_serialized), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
	user_tuple = db.session.execute(db.select(User).filter_by(id = user_id)).one_or_none()
	if user_tuple is None:
		return jsonify({"message": "User doesn't exist"}), 400
	user = user_tuple[0]
	return jsonify(user.serialize()), 200

@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
	user_tuple = db.session.execute(db.select(User).filter_by(id = user_id)).one_or_none()
	if user_tuple is None:
		return jsonify({"message": "User doesn't exist"}), 400
	
	favorites_list = []
	favorites_query = db.session.execute(db.select(Favorite).filter_by(user_id=user_id)).scalars().all()
	for favorite in favorites_query:
		favorite_data = {
			"id": favorite.id,
			"user_id": favorite.user_id,
			"character_id": favorite.character_id,
			"planet_id": favorite.planet_id
		}
		favorites_list.append(favorite_data)
	return jsonify({"favorites": favorites_list}), 200

#   +++ CHARACTER/PEOPLE +++
@app.route("/people", methods=["POST"])
def create_character():
	data = request.json
	name = data.get("name")
	birth_year = data.get("birth_year")
	species = data.get("species")
	height = data.get("height")
	mass = data.get("mass")
	gender = data.get("gender")
	hair_color = data.get("hair_color")
	skin_color = data.get("skin_color")
	homeworld = data.get("homeworld")

	if name == None:
		return jsonify({
			"message": "Character's name is required"
		}), 400
	character_already_exist = db.session.execute(db.select(Character).filter_by(name=name)).one_or_none()
	if character_already_exist:
		return jsonify({
			"message": "Character already exist"
		}), 400
	new_character = Character(name, birth_year, species, height, mass, gender, hair_color, skin_color, homeworld)
	if not isinstance(new_character, Character):
		return jsonify ({
			"message": "Server error... Try again later"
		})
	try:
		db.session.add(new_character)
		db.session.commit()
	except:
		return jsonify({
			"message": "Database error"
		}), 500
	character_serialized = new_character.serialize()
	return jsonify(character_serialized), 201

@app.route("/people", methods=["GET"])
def get_characters():
	characters_result = db.session.execute(db.select(Character)).all()
	characters = []
	for character_tuple in characters_result:
		characters.append(character_tuple[0])
	characters_serialized = []
	for character in characters:
		characters_serialized.append(character.serialize())
	return jsonify(characters_serialized), 200

@app.route("/people/<int:character_id>", methods=["GET"])
def get_character(character_id):
	character_tuple = db.session.execute(db.select(Character).filter_by(id = character_id)).one_or_none()
	if character_tuple is None:
		return jsonify({"message": "Character doesn't exist"}), 400
	character = character_tuple[0]
	return jsonify(character.serialize()), 200

#   +++ PLANETS +++
@app.route("/planets", methods=["POST"])
def create_planet():
	data = request.json
	name = data.get("name")
	population = data.get("population")
	rotation_period = data.get("rotation_period")
	orbital_period = data.get("orbital_period")
	diameter = data.get("diameter")
	gravity = data.get("gravity")
	terrain = data.get("terrain")
	surface_water = data.get("surface_water")
	climate = data.get("climate")

	if name == None:
		return jsonify({
			"message": "Planet's name is required"
		}), 400
	planet_already_exist = db.session.execute(db.select(Planet).filter_by(name=name)).one_or_none()
	if planet_already_exist:
		return jsonify({
			"message": "Planet already exist"
		}), 400
	new_planet = Planet(name, population, rotation_period, orbital_period, diameter, gravity, terrain, surface_water, climate)
	if not isinstance(new_planet, Planet):
		return jsonify ({
			"message": "Server error... Try again later"
		})
	try:
		db.session.add(new_planet)
		db.session.commit()
	except:
		return jsonify({
			"message": "Database error"
		}), 500
	planet_serialized = new_planet.serialize()
	return jsonify(planet_serialized), 201

@app.route("/planets", methods=["GET"])
def get_planets():
	planets_result = db.session.execute(db.select(Planet)).all()
	planets = []
	for planet_tuple in planets_result:
		planets.append(planet_tuple[0])
	planets_serialized = []
	for planet in planets:
		planets_serialized.append(planet.serialize())
	return jsonify(planets_serialized), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
	planet_tuple = db.session.execute(db.select(Planet).filter_by(id = planet_id)).one_or_none()
	if planet_tuple is None:
		return jsonify({"message": "Planet doesn't exist"}), 400
	planet = planet_tuple[0]
	return jsonify(planet.serialize()), 200

#   +++ FAVORITES +++
@app.route("/favorite/<string:category>/<int:elem_id>", methods=["POST"])
def add_favorite(category, elem_id):
	data = request.json
	user_id = data.get("user_id")
	if not user_id:
		return jsonify({"message": "User is required"}), 400
	
	if category not in ["people", "planet"]:
		return jsonify({"message": "Invalid category"}), 400

	if category == "people":
		character_id = elem_id
		planet_id = None

	if category == "planet":
		character_id = None
		planet_id = elem_id

	#Verificamos si el elememto extiste en People o Planets
	if category == "people":
		element = db.session.execute(db.select(Character).filter_by(id=elem_id)).scalar_one_or_none()
		if not element:
			return jsonify({"message": "Character not found"}), 404
	else:
		element = db.session.execute(db.select(Planet).filter_by(id=elem_id)).scalar_one_or_none()
		if not element:
			return jsonify({"message": "Planet not found"}), 404
		
	#Verificamos si ya existe en Favoritos
	existing_favorite = db.session.execute(db.select(Favorite).filter_by(user_id=user_id,
		**({
			"character_id": elem_id if category == "people" else None,
			"planet_id": elem_id if category == "planet" else None
		})
	)).one_or_none()
	if existing_favorite:
		return jsonify({"message": "Already in Favorites"}), 400
	
	new_favorite = Favorite(user_id, character_id, planet_id)
	if not isinstance(new_favorite, Favorite):
		return jsonify ({
			"message": "Server error... Try again later"
		})
	
	try:
		db.session.add(new_favorite)
		db.session.commit()
	except:
		return jsonify({
			"message": "Database error"
		}), 500
	
	favorite_serialized = new_favorite.serialize()
	return jsonify(favorite_serialized), 201

#+++++++++++++++++++++++++++++++++++++++++++++
@app.route('/favorite/<string:category>/<int:elem_id>', methods=['DELETE'])
def remove_favorite(category, elem_id):
	data = request.json
	user_id = data.get("user_id")
	if not user_id:
		return jsonify({"message": "User is required"}), 400

	if category not in ["people", "planet"]:
		return jsonify({"message": "Invalid category"}), 400

	if category == "people":
		character_id = elem_id
		planet_id = None

	if category == "planet":
		character_id = None
		planet_id = elem_id

	favorite = db.session.execute(db.select(Favorite).filter_by(user_id=user_id,
		**({
			"character_id": elem_id if category == "people" else None,
			"planet_id": elem_id if category == "planet" else None
		})
	)).one_or_none()
	if not favorite:
		return jsonify({"message": "Element not found"}), 404
	
	try:
		db.session.delete(favorite[0])
		print("**************************")
		db.session.commit()
		print("**************************")
	except:
		return jsonify({
			"message": "Database error"
		}), 500

	return jsonify({"message": "Favorite deleted"}), 201
#+++++++++++++++++++++++++++++++++++++++++++++

#Modificar la ruta para que sea dinámica
@app.route("/favorite", methods=["GET"])
def get_favorites():
	favorites_result = db.session.execute(db.select(Favorite)).all()
	favorites = []
	for favorite_tuple in favorites_result:
		favorites.append(favorite_tuple[0])
	favorites_serialized = []
	for favorite in favorites:
		favorites_serialized.append(favorite.serialize())
	return jsonify(favorites_serialized), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
