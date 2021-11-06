## This method will now be modified to connect to a database variable instead of a dict/in memory object

from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    # Get the user from the DB Class object directly from user.py
    user = UserModel.find_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    # Get the user id from the DB Class object directly from user.py and map it to identity of the payload
    user_id = payload["identity"]
    return UserModel.find_by_userid(user_id)

#print(authenticate("Lauren","Admin123"))