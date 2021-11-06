## Create the user dict equivanlent Object
## This can be imported to the security module

## Complete the object by connecting it to a database

from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, 
    help="Please enter the username of the user")
    parser.add_argument("password", type=str, required=True, 
    help="Please enter the password for the user")
    def post(self):
        data = UserRegister.parser.parse_args()
        return UserModel.register_user(UserModel(**data))