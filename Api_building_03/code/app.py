'''
    This is section 5.
    Working with database (sql-lite).
'''

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from user import UserRegister
from security import authenticate, identity
from item import Item, ItemList
import create_table

app = Flask(__name__)
app.secret_key = "mySecreteKey"
api = Api(app)
jwt = JWT(app, authenticate, identity)      # app use both auth and identity to allow user


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

