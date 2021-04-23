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
from models import db, User, Person, Planet, Starship
#from models import Person, Planet, Starship
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
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


# USER ROUTES

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).first()
    if user is None or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/user', methods=['GET'])
@jwt_required()
def handle_hello():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "user": user.serialize()
    }

    return jsonify(response_body), 200 

@app.route('/user', methods=['POST'])
def handle_user():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /user response ",
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# PERSON ROUTES
    
@app.route('/person', methods=['GET'])
def person():
    person = Person.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /people response ",
        "person": person.serialize()
    }

    return jsonify(response_body), 200


@app.route('/person', methods=['POST'])
def handle_person():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /people response ",
        "person": person.serialize()
    }

    return jsonify(response_body), 200   

# PLANET ROUTES

@app.route('/planet', methods=['GET'])
def planet():
    name = Planet.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "name": name.serialize()
    }

    return jsonify(response_body), 200  


@app.route('/planet', methods=['POST'])
def handle_planet():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /planet response ",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200   

# STARSHIP ROUTES

@app.route('/starship', methods=['GET'])
def starship():
    name = Starship.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /starship response ",
        "name": name.serialize()
    }

    return jsonify(response_body), 200 


@app.route('/starship', methods=['POST'])
def handle_starship():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /starship response ",
        "starship": starship.serialize()
    }

    return jsonify(response_body), 200




# DELETE ROUTES - NOT NEEDED FOR THIS PROJECT

# @app.route('/people/<int:id>', methods=['DELETE'])
# def delete_people(id):
#     people.pop(id)
#     return jsonify(people), 200


# @app.route('/planet/<int:id>', methods=['DELETE'])
# def delete_planet(id):
#     planet.pop(id)
#     return jsonify(planet), 200


# @app.route('/starship/<int:id>', methods=['DELETE'])
# def delete_starship(id):
#     starship.pop(id)
#     return jsonify(starship), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
