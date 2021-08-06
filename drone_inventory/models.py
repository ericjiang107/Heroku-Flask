# anything with flask_ is a wrapper, different way to build it 
from flask_sqlalchemy import SQLAlchemy # <---- a wrapper for SQLAlchemy (query, etc)
from flask_migrate import Migrate # <--- a wrapper for Migrate and Migrate makes it easier to change database models/information
from datetime import datetime
import uuid # <---- provides a unique identifier (string)

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash # <---- part of flask. Tools to hash password so when storing passwords, it
# converts it to a hash value so others can't see your actual password 

# Creates hex tokens for our API access
import secrets 

# imports login manager from flask_login package
from flask_login import LoginManager, UserMixin

# import for mashmallow marshaller
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True) # the data type can only have varchar of 150 characters and nullable means it cannot be blank
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # automatically default to whatever the time is right now
    drone = db.relationship('Drone', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = "", id = ""):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


class Drone(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    camera_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self,name,description,price, camera_quality,flight_time,max_speed,dimensions, weight,cost_of_prod,series,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token


    def set_id(self):
        return (secrets.token_urlsafe()) # generate a random url text string 

# Creating our Marshaller to pull k,v pairs out of Drone instance attributes
class DroneSchema(ma.Schema):
    class Meta:
        # detailing which fields to pull out of our drone and send to API call and vice versa
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']
    
    # take a python class object like <Drone x27451298509563>
    # iterates through our fields and adds them to a dictionary 

    # ex:
    # {
    #   'id': drone_1.id
    #   'name': drone_1.name
    #   'description': drone_1.description
    # }

# instantiating:
drone_schema = DroneSchema()
drones_schema = DroneSchema(many=True)

