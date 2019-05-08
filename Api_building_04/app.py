'''
    This is section 6.
    working with Flask SQLAlchemy

    install:-
        pip install Flask-SQLAlchemy
'''

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList
import create_table

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # sqlalchemy will live at root directory

''' 
    essentially, something is changed but not been saved to database, the extension flask_alchemy
    was tracking every changed and took some resources.
    here, we are turning off because sqlAlchemy itself the main library has modification tracker,
    which is better.
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "mySecreteKey"
api = Api(app)
jwt = JWT(app, authenticate, identity)      # app use both auth and identity to allow user


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    '''
        we are importing here as because a things called circular imports.
        your itemModels is also using db, to it will create circular import between db and itemModel.
    '''
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

