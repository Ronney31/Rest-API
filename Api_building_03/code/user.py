# user object
import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"

        # second parameter is necessary to be a tuple
        result = cursor.execute(query, (username,))

        # this will get the first row
        row = result.fetchone()
        user = None
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"

        # second parameter is necessary to be a tuple
        result = cursor.execute(query, (_id,))

        # this will get the first row
        row = result.fetchone()
        user = None
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)

        connection.close()
        return user


# creating endpoint to create new user
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        # checking if the user is already exits of not.
        if User.find_by_username(data['username']):
            return {"Message": "User Already Exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"Message": "User Created Successfully."}, 201
