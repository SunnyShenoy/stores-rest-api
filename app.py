from flask import Flask
from flask_restful import Api
from resources.user import UserRegister
## Adding Authentication mechanism using Flask_JWT and user defined security module
from flask_jwt import JWT
## Add authorization using JWT/Bearer token mechanism
from security import authenticate, identity
from resources.items import *
from resources.store import *
import os

#os.chdir("C:\Python\Project1\Flask_Application\SQLAlchemy\Code")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items_data.db'
app.config['SQLALCHEMY_BINDS'] = {'db_two': 'sqlite:///user_data.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_val'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(items, "/items")  # /items
api.add_resource(item, "/item/<string:name>") # /item
api.add_resource(UserRegister, "/Register")  # /Register
api.add_resource(stores, "/stores") # /stores
api.add_resource(store, "/store/<string:name>") # /store


# Make sure the Flask application only starts if called directly via app.py

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True) # Run Flask application
