from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

'''
The following setup is required with SQLAlchemy:
1. setup a db object for SqlAlchemy --> db.py
2. initialize the sqlalchemy object on app before starting up Flask app using
        db.init_app(app)  --> app.py
3. Import the SQLAlchemy object on app.py, items and users --> items.py, users.py
4. Inherit the ItemModel and UserModel from db.Model class for using SQLAlchemy
5. Create table using __tablename__
6. Setup DB column - Variable links on Model scripts
7. Finally set app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] to false to use the 
    default SQLAlchemy track notifications and turn off the flask-sqlalchemy notifications tracker
'''