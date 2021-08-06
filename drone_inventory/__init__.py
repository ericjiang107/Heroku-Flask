# Everything in here is similar to a class where when you insantiate this, everything inside is insantiated

from flask import Flask 
# from config import Config 
from .site.routes import site
from .authentication.routes import auth
from config import Config
from flask_migrate import Migrate
from .models import db, login_manager, ma
from .api.routes import api
from .helpers import JSONEncoder
from flask_cors import CORS

app = Flask(__name__) # the name of the directory that is housing it. The __name__ takes on the name of the directory that it is in
app.config.from_object(Config) # This is an environment variable -- configure app with any variables 

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

db.init_app(app)

login_manager.init_app(app)
ma.init_app(app)

login_manager.login_view = 'auth.signin' # Specify what page to load for NON-AUTHED users

migrate = Migrate(app, db)

app.json_encoder = JSONEncoder

CORS(app)

from .models import User