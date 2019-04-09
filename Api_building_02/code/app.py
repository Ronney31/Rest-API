'''
    This is section 4.

    For this project, please follow the step
    I am using PyCharm, which creates environment by it's own. but if not use new need to create an environment.
    basically environment will replicate a fresh copy of the python and it's library, so that any change in original
    installed version of the python or the libraries will not effect our project.
    Now, after creating environment.
    1. pip install Flask-RESTful
    2. pip freeze ( to see the versions and libraries installed )
    3. pip install Flask-JWT    ( For authentication JSON WEB TOKEN)

    **Every Resource will be our class, and API will deal with resources.
'''

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required   # to work without app
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "mySecreteKey"
api = Api(app)

jwt = JWT(app, authenticate, identity)      # app use both auth and identity to allow user
'''
    JWT will create a new end point /auth
    calling /auth jwt send both to security and compare there.
'''

items = []

"""class Student(Resource):  # Resource

    '''
        @app.route('/student'),
        not required anymore as we are doing
        api.add_resource(Student, '/student/<string:name>')
    '''

    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>')  # http://127.0.0.1:5000/student/Ranjan
"""


class Item(Resource):  # Resource
    # now parser is class variable to the calling would be using class name.
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    '''
        The authenticate will return a JWT token and send that to identity and this will send correct user
        details.
        TO Test:
            Going to Insominia, POST /auth will contain the username and password in json formant wil be will send
            and authentication will be performed and that will return jwt_token (encrypted data).
            This jwt_token we will use in GET /item/<name> .
                Setting:- Inside Header we say:- Authorization
                          Inside Value we say :- JWT jwt_token
            and then the get will work.
        **Note:- to add item before testing, and remember to provide endpoint of added item inside GET /item/<name>
        
        We can use @jwt_required() for all the function and thereafter only with the jwt_token those endpoint would
        be allowed to access.
    '''
    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {'item': None}, 404  # https status code 404 not found

        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):

        if next(filter(lambda x: x['name'] == name, items), None):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400  # 400 is bad request
        # data = request.get_json()
        ''' 
            as a parameter of request.get_json(), force=True means not always json needed for user
            silent=True return NONE 
        '''
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # https status code 201 for created

    def delete(self, name):
        global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}

        if next(filter(lambda x: x['name'] == name, items), None):
            items = list(filter(lambda x: x['name'] != name, items))
            return {'message': 'Item deleted'}, 200
        return {'message': 'Not Found'}, 404

    def put(self, name):    # will create or update item
        '''
            Here we are using parser so that we user can pass only the price in our case nothing else
            then that, like i tried passing 'another' from insominia application but the through error.
            This is good, to restrict the api to accept only the required field not others.
            header file:- from flask_restful import reqparse
        '''
        #  now we made parser as class variable
        '''
            parser = reqparse.RequestParser()
            parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
        '''
        data = Item.parser.parse_args()
        # print (data['another'])
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')

app.run(port=5000, debug=True)

