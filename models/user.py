# Use SQLAlchemy
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'db_two'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, username, password):

        self.username = username
        self.password = password

    def json(self):
        return {"username": self.username, "password": self.password}

    @classmethod
    def register_user(cls, userdata):
        '''
        Note that all the code of sqlite can be replaced with a single line of sqlalchemy
        SQLAlchemy 
        '''
        result = cls.query.filter_by(username=userdata.username).first()

        if not result:
            db.session.add(userdata)
            db.session.commit()
            return {
                "user data": userdata.json(),
                "Comments": {"Success": "User Created"}
            }, 201
        else:
            return {"Error": "User already exists"}, 400

    @classmethod
    def find_by_username(cls, username):
        '''
        Note that all the code of sqlite can be replaced with a single line of sqlalchemy
        SQLAlchemy 
        '''
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(id=userid).first()
