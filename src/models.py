from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define association tables to create a many to many for the favorites
favorites_people = db.Table('user_people', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)
favorites_planets = db.Table('user_planets', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)
favorites_starships = db.Table('user_starships', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('starships_id', db.Integer, db.ForeignKey('starships.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False) 
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    people = db.relationship("Person", secondary=favorites_people)
    planets = db.relationship("Planet", secondary=favorites_planets)
    starships = db.relationship("Starship", secondary=favorites_starships)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_people": list(map(lambda x: x.serialize(), self.people)),
            "favorite_planets": list(map(lambda x: x.serialize(), self.planets)),
            "favorite_starships": list(map(lambda x: x.serialize(), self.starships))
            # do not serialize the password, its a security breach
        }                               

class Person(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the People   
    id = db.Column(db.Integer, primary_key=True)
    # one to one with planet for homeworld
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    height = db.Column(db.String(50))
    mass = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    photo_url: db.Column(db.String)      

    def __repr__(self):
        return '<Person %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld.name,
            "height": self.height
        }   

class Planet(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the Planets   
    id = db.Column(db.Integer, primary_key=True)
    # relationship for the homeworld for people
    people = db.relationship("Person", backref='homeworld', lazy=True)
    diameter = db.Column(db.String(50))
    rotation_period = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    population = db.Column(db.String(50))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    photo_url: db.Column(db.String)

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Starship(db.Model):
    __tablename__ = 'starships'
    # Here we define columns for the Starships   
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    starship_class = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    cost_in_credits = db.Column(db.String(50))
    length = db.Column(db.String(50))
    crew = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    max_atmosphering_speed = db.Column(db.String(50))
    hyperdrive_rating = db.Column(db.String(50))
    MGLT = db.Column(db.String(50))
    cargo_capacity = db.Column(db.String(50))
    consumables = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    photo_url: db.Column(db.String)

    def __repr__(self):
        return '<Starship %r>' % self.name
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }    