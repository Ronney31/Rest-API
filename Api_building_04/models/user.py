import sqlite3
from db import db
# helper
# Models package/folder is our internal representation of an entity.


class UserModel(db.Model):
    __tablename__ = 'users'
    ''' telling SQLAlchemy that their is col named id which is primary_key and Integer. '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
        # self.otherParameters = "hi"  # this wouldn't be stored in db, it will stay in object.

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

