from functools import wraps # wraps allow us to create our own decorators inside our own functions
import secrets 
from flask import request, jsonify 
from drone_inventory.models import User, Drone

# to create a decorator -- need to create a function first
def token_required(our_flask_function):
    @wraps(our_flask_function) # <--- decorator
    def decorated(*args, **kwargs): # kwargs are keyword arguments
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401 

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
        except: # if it does not occur
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Invalid Token, try again'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

import decimal
from flask import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert any decimal values (price, cost_of_prod)
            return str(obj)
        return super(JSONEncoder,self).default(obj) # super means if default doesn't occur here, rerun 