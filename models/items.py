## Using SQLAlchemy
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, _type, price, store_id):
        self.name = name
        self.type = _type
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"Name": self.name, "Type": self.type, "Price": self.price, "Store_id": self.store_id}

    @classmethod
    def get_item(cls, name):
        
        item_row = cls.query.filter_by(name=name).first()

        if item_row:
            return item_row, 200
            #return { "item": item_row.json()}, 200
        else:
            return {"Error:": f"{name} does not exist"}, 404
        '''
        This can be chained in the following ways to write complex queries
        Eq for : SELECT * from __tablename__ where name = name (limit 1)
        a. ItemModel.query.filter_by(name=name).filter_by(id=1)   --> chaining
        OR
        b. ItemModel.query.filter_by(name=name, id=1)  --> arguments
        
        Note: chaining is important to add other filtering such as limit, order etc
        ItemModel.query.filter_by(name=name).filter_by(id=1).first()
        '''

    def write_item(self):
        
        item_row = self.query.filter_by(name=self.name).first()

        db.session.add(self)
        db.session.commit()

        if not item_row:
            return {self.name: self.json(), "message": "New item created."}, 201
        else:
            return {self.name: self.json(), "message": "Item existed. Has been overwritten."}, 200

    def delete_item(self):

        db.session.delete(self)
        db.session.commit()

        return {self.name: self.json(), "message": "Item Deleted successfully."}, 200