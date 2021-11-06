from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt import jwt_required  ## This did not work without JWT_ext package
import random

'''
1. import JWT and jwt_required modules from flask_jwt
2. Setup app.secretkey
3. setup /auth using jwt = JWT(<your app>, authenticate to get user, identity to process payload)
4. Add @jwt_required() decorator if you want to add authentication
'''
class stores(Resource):
    def get(self):
        return {"stores_array": [i.json() for i in StoreModel.query.all()]}, 200
        ## This can also be written as a list comprehension or a map
        # return {"items_array": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200

class store(Resource):
    '''
    This ensures that only the required input data is passed and rest is ignored. Steps are: 
    1. define parser variable
    2. add arguments
    3. parse arguments
    '''

    parser = reqparse.RequestParser()
    parser.add_argument('Name', type=str,
    help="This field marks the name of the store to be updated")
    parser.add_argument('Id', type=int,
    help="This field marks the store id to be updated")

    @jwt_required()
    def get(self, name):
        try:
            ret_item, error_code = StoreModel.get_store(name)
            if error_code == 200:
                return { "item": ret_item.json()}, error_code
            else:
                return ret_item, error_code
        except:
            return {"Error:": "Get Operation failed"}, 500

    def post(self, name):
        try:
            _, error_code = StoreModel.get_store(name)

            if error_code == 200:
                return {"Error": "Item already exists"}, 400
            else:
                my_id = random.randint(0,999999)
                dict_item = StoreModel(my_id, name)
                return dict_item.create_store()
        except:
            return {"Error:": "Post Operation failed"}, 500

    def put(self, name):
        try:
            get_item, error_code = StoreModel.get_store(name)
            if error_code != 200:
                my_id = random.randint(0,999999)
                upd_item = StoreModel(my_id, name)
                return upd_item.create_store()
            else:
                upd_value = store.parser.parse_args()
                if upd_value["Name"]:
                    get_item.store_name = upd_value["Name"]
                    get_item.id = upd_value["Id"]
                    return get_item.create_store()
                else:
                    return {"Error": "Item already exists, Please enter params to update if required."}, 400
        except:
            return {"Error:": "Put Operation failed"}, 500

    def delete(self, name):
        try:
            my_item, error_code = StoreModel.get_store(name)

            if error_code != 200:
                return {"Error:": f"{name} does not exist"}, 404
            else:
                return my_item.delete_store()
        except:
            return {"Error:": "Delete Operation failed"}, 500
