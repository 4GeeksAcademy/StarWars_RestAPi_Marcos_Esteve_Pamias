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
from models import db, User, Characters, Planets, Favorite_Character, Favorite_Planet
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



####### GET USERS #######

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users= User.query.all()
    results = list(map(lambda usuario: usuario.serialize(), all_users))
    print(results)
    if not results:
        response_body = {
            "msg" : "No existen datos"
        }
        return jsonify(response_body),200
    
    return jsonify(results), 200

#####GET USER FAVORITES#####
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        # Obtengo todos personajes y planetas favoritos en una sola consulta utilizando join
        favorite_characters = db.session.query(Characters).join(Favorite_Character).filter(Favorite_Character.user_id == user_id).all()
        favorite_planets = db.session.query(Planets).join(Favorite_Planet).filter(Favorite_Planet.user_id == user_id).all()

        favorite_characters_data = [character.serialize() for character in favorite_characters]
        favorite_planets_data = [planet.serialize() for planet in favorite_planets]

        return jsonify({
            "characters": favorite_characters_data,
            "planets": favorite_planets_data,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###### GET PEOPLE/Characters #####

@app.route('/people', methods=['GET'])
def get_people():
    all_people = Characters.query.all()
    result = list(map(lambda person: person.serialize(), all_people))
    if not result:
        return jsonify({"msg": "No existen datos"}), 200
    return jsonify(result), 200

####GET ONE CHARACTER/PEOPLE#####
@app.route('/peolple/<int:characters_id>', methods = ['GET'])
def get_one_character(characters_id):
    one_character = Characters.query.filter_by(id=characters_id).first()
    if one_character:
        return jsonify(one_character.serialize()), 200
    return jsonify({"msg": "Error, no existe personaje"})

####GET FAVORITE CHARACTER#####
@app.route('/favorite/character/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):
    try:
        # Validar la existencia del user_id en el cuerpo de la solicitud
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        user = User.query.get_or_404(user_id)
        character = Characters.query.get_or_404(characters_id)
        
        # Comprobar si ya tengo un favorito
        favorite_exist = Favorite_Character.query.filter_by(user_id=user_id, characters_id=characters_id).first()
        if favorite_exist:
            return jsonify({"error": "This character is already a favorite"}), 400

        # Creo y añado el nuevo favorito
        new_favorite = Favorite_Character(
            user_id=user_id,
            characters_id=characters_id,
            user_characteristics=f'{user.name} likes {character.name}'
        )
        
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(new_favorite.serialize()), 200

    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500


####GET ALL Planet####
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = list(map(lambda planet: planet.serialize(), all_planets))
    if not result:
        return jsonify({"msg": "No existen datos"}), 200
    return jsonify(result), 200

####GET ONE Planet####
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    try:
        one_planet = Planets.query.filter_by(id=planets_id).first()
        if one_planet:
            return jsonify(one_planet.serialize()), 200
        return jsonify({"msg": "Error, no existe planeta"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


####GET FAVORITE PLANET#####
@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):
    try:
        # Validar la existencia del user_id en el cuerpo de la solicitud
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        user = User.query.get_or_404(user_id)
        planet = Planets.query.get_or_404(planets_id)
        
        # Comprobar si ya hay un favorito
        favorite_exist = Favorite_Planet.query.filter_by(user_id=user_id, planets_id=planets_id).first()
        if favorite_exist:
            return jsonify({"error": "This planet is already a favorite"}), 400

        # Creo y añado el nuevo favorito
        new_favorite = Favorite_Planet(
            user_id=user_id,
            planets_id=planets_id,
            user_characteristics=f'{user.name} likes {planet.name}'
        )
        
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(new_favorite.serialize()), 200

    except Exception as e:
        db.session.rollback()  # Revertir la sesión en caso de error
        return jsonify({"error": str(e)}), 500

#####DELETE Favorite Planet#####
@app.route('/favorite/planet/<int:favorite_planet_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_planet_id):

    favorite_planet = Favorite_Planet.query.filter_by(id=favorite_planet_id).first()
    if favorite_planet is None:
        return jsonify("ERROR: This is not the planet you are looking for"), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify(favorite_planet.serialize()), 200

#####DELETE Favorite Character#####
@app.route('/favorite/character/<int:favorite_character_id>', methods=['DELETE'])
def delete_favorite_character(favorite_character_id):

    favorite_character = Favorite_Character.query.filter_by(id=favorite_character_id).first()
    if favorite_character is None:
        return jsonify("ERROR: This is not the character you are looking for"), 404

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify(favorite_character.serialize()), 200


 
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
