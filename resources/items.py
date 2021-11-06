from flask import Flask
from flask_restful import Resource, reqparse
from models.items import ItemModel
from models.store import StoreModel
from flask_jwt import jwt_required  ## This did not work without JWT_ext package

'''
1. import JWT and jwt_required modules from flask_jwt
2. Setup app.secretkey
3. setup /auth using jwt = JWT(<your app>, authenticate to get user, identity to process payload)
4. Add @jwt_required() decorator if you want to add authentication
'''
class items(Resource):
    def get(self):
        return {"items_array": [item.json() for item in ItemModel.query.all()]}, 200
        ## This can also be written as a list comprehension or a map
        # return {"items_array": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200

class item(Resource):
    '''
    This ensures that only the required input data is passed and rest is ignored. Steps are: 
    1. define parser variable
    2. add arguments
    3. parse arguments
    '''

    parser = reqparse.RequestParser()
    parser.add_argument('Type', type=str, required=True,
    help="This filed tells us about the item and is mandatory")
    parser.add_argument('Price', type=float, required=True, 
    help="This field indicates price and is mandatory")
    parser.add_argument('Store_id', type=int, required=True,
    help="Adds the store id foreign key of the item")

    @jwt_required()
    def get(self, name):
        try:
            ret_item, error_code = ItemModel.get_item(name)
            if error_code == 200:
                return { "item": ret_item.json()}, error_code
            else:
                return ret_item, error_code
        except:
            return {"Error:": "Get Operation failed"}, 500

    def post(self, name):
        try:
            _, error_code = ItemModel.get_item(name)

            if error_code == 200:
                return {"Error": "Item already exists"}, 400
            else:
                my_item = item.parser.parse_args()  # -> Make sure to add the class name as it is now a class property
                _, error_code = StoreModel.get_store_id(my_item['Store_id'])
                if error_code != 200:
                    return {"Error": f"Store ID {my_item['Store_id']} does not exist"}, 400
                dict_item = ItemModel(name, my_item['Type'], my_item['Price'], my_item['Store_id'])
                return dict_item.write_item()
        except:
            return {"Error:": "Post Operation failed"}, 500

    def put(self, name):
        try:
            get_item, error_code = ItemModel.get_item(name)
            my_item = item.parser.parse_args()  # -> Make sure to add the class name as it is now a class property
            _, store_code = StoreModel.get_store_id(my_item['Store_id'])

            if store_code != 200:
                return {"Error": f"Store ID {my_item['Store_id']} does not exist"}, 400

            if error_code != 200:
                upd_item = ItemModel(name, my_item['Type'], my_item['Price'], my_item['Store_id'])
                return upd_item.write_item()
            else:
                get_item.type = my_item['Type']
                get_item.price = my_item['Price']
                get_item.store_id = my_item['Store_id']
                return get_item.write_item()
        except:
            return {"Error:": "Put Operation failed"}, 500

    def delete(self, name):
        try:
            my_item, error_code = ItemModel.get_item(name)

            if error_code != 200:
                return {"Error:": f"{name} does not exist"}, 404
            else:
                return my_item.delete_item()
        except:
            return {"Error:": "Delete Operation failed"}, 500
