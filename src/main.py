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
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Below app sets up the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this later!
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
        return jsonify({"msg": "Incorrect username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# PUT request used to send data to the API to update or create user
@app.route('/user', methods=['PUT']) 
def update_user_favorites():
    user_id = request.json.get("user_id", None)
    resource_id = user_id = request.json.get("id", None)
    resource_type = user_id = request.json.get("type", None)

    user = User.query.get(user_id)

    if resource_type == "person":
        resource = Person.query.get(resource_id)
        user.people.append(resource)    

    if resource_type == "planet":
        resource = Planet.query.get(resource_id)
        user.planets.append(resource) 

    if resource_type == "starship":
        resource = Starship.query.get(resource_id)
        user.starships.append(resource)

    if user_id is None:
        return jsonify({"msg": "Missing required parameter user_id"}), 401

    if user is None:
        return jsonify({"msg": "Could not find specified user"}), 404

    if resource_id is None:
        return jsonify({"msg": "Missing required parameter id"}), 401

    if resource_type is None:
        return jsonify({"msg": "Missing required parameter type"}), 401      

    db.session.commit()            
    
    response_body = {
        "msg": "Resource added successfully",
        "user": user.serialize()
    }
        
# GET request used to retreive data from server from user
@app.route('/user', methods=['GET'])
# @jwt_required()
def retrive_user():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /user response",
        "user": user.serialize()
    }

    return jsonify(response_body), 200 

# POST request used to send data to the API to create or udpate user
@app.route('/user', methods=['POST'])
def handle_user():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /user response",
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# PERSON ROUTES

# GET request used to retreive data from server from person
@app.route('/person', methods=['GET'])
def retrive_person():
    person = Person.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /people response",
        "person": person.serialize()
    }

    return jsonify(response_body), 200

# POST request used to send data to the API to create or udpate person
@app.route('/person', methods=['POST'])
def handle_person():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /people response",
        "person": person.serialize()
    }

    return jsonify(response_body), 200   

# PLANET ROUTES

# GET request used to retreive data from server from planet
@app.route('/planet', methods=['GET'])
def retrive_planet():
    name = Planet.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /planet response",
        "name": name.serialize()
    }

    return jsonify(response_body), 200  

# POST request used to send data to the API to create or udpate planet
@app.route('/planet', methods=['POST'])
def handle_planet():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /planet response",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200   

# STARSHIP ROUTES

# GET request used to retreive data from server from starship
@app.route('/starship', methods=['GET'])
def retrive_starship():
    name = Starship.query.get(1)
    response_body = {
        "msg": "Hello, this is your GET /starship response",
        "name": name.serialize()
    }

    return jsonify(response_body), 200 

# POST request used to send data to the API to create or udpate starship
@app.route('/starship', methods=['POST'])
def handle_starship():
    user = User.query.get(1)
    response_body = {
        "msg": "Hello, this is your POST /starship response",
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
