## Using SQLAlchemy
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(120))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, _id:int, store_name):
        self.id = _id
        self.store_name = store_name

    def json(self):
        return {"Store_Id": self.id, "Store_Name": self.store_name, "Items": [i.json() for i in self.items.all()]}

    @classmethod
    def get_store(cls, name):
        
        store_row = cls.query.filter_by(store_name=name).first()

        if store_row:
            return store_row, 200
            #return { "item": item_row.json()}, 200
        else:
            return {"Error:": f"{name} does not exist"}, 404

    @classmethod
    def get_store_id(cls, _id):
        
        store_row = cls.query.filter_by(id=_id).first()

        if store_row:
            return store_row, 200
            #return { "item": item_row.json()}, 200
        else:
            return {"Error:": f"{_id} does not exist"}, 404
        '''
        This can be chained in the following ways to write complex queries
        Eq for : SELECT * from __tablename__ where name = name (limit 1)
        a. ItemModel.query.filter_by(name=name).filter_by(id=1)   --> chaining
        OR
        b. ItemModel.query.filter_by(name=name, id=1)  --> arguments
        
        Note: chaining is important to add other filtering such as limit, order etc
        ItemModel.query.filter_by(name=name).filter_by(id=1).first()
        '''

    def create_store(self):
        
        item_row = self.query.filter_by(store_name=self.store_name).first()
        print(self.store_name, self.id)
        db.session.add(self)
        db.session.commit()

        if not item_row:
            return {self.store_name: self.json(), "message": "New Store created."}, 201
        else:
            return {self.store_name: self.json(), "message": "Store existed. Has been overwritten."}, 200

    def delete_store(self):

        db.session.delete(self)
        db.session.commit()

        return {self.store_name: self.json(), "message": "Store Deleted successfully."}, 200