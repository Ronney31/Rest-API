# user object
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


# creating endpoint to create new user
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        # checking if the user is already exits of not.
        if UserModel.find_by_username(data['username']):
            return {"Message": "User Already Exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"Message": "User Created Successfully."}, 201
