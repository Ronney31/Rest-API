from flask_restful import Api
from flask import Flask
from resources.userData import uData, allUserData
app = Flask(__name__)
api = Api(app)


api.add_resource(uData, '/iki/<userName>')
api.add_resource(allUserData, '/ikis/users/')

if __name__ == "__main__" :
    from resources import database
    app.run(port=5010, debug=True)
