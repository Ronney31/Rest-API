import sqlite3

connection = sqlite3.connect('resources/data.db')

cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (username text, ans1 text, ans2 text, ans3 text, ans4 text)"
cursor.execute(create_table)

connection.commit()
connection.close()


class databaseModel():
    def __init__(self, username, q1,q2,q3,q4):
        self.username = username
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def json(self):
        jsonData = {'userName': self.username, 'Answer 1': self.q1, 'Answer 2': self.q2, 'Answer 3': self.q3, 'Answer 4': self.q4}
        return jsonData


    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('resources/data.db')
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
    def insert_data(cls, username, answers):
        connection = sqlite3.connect('resources/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (username, answers["q1"], answers["q2"], answers["q3"], answers["q4"]))
        connection.commit()
        connection.close()

    @classmethod
    def update_data(cls, username, answers):
        connection = sqlite3.connect('resources/data.db')
        cursor = connection.cursor()
        query = "UPDATE users SET ans1=?, ans2=?, ans3=?, ans4=? WHERE username=?"
        cursor.execute(query, (answers["q1"], answers["q2"], answers["q3"], answers["q4"], username))
        connection.commit()
        connection.close()

    @classmethod
    def select_all(cls):
        connection = sqlite3.connect('resources/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'userName': row[0], 'Answer 1': row[1], 'Answer 2': row[2], 'Answer 3': row[3], 'Answer 4': row[4]})
        connection.commit()
        connection.close()
        return items

    @classmethod
    def delete_user(cls, username):
        if cls.find_by_username(username):
            connection = sqlite3.connect('resources/data.db')
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE username=?"
            cursor.execute(query, (username,))
            connection.commit()
            connection.close()
            return {'message': 'User deleted'}
        return {'message': 'Not Found'}
