import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        try:
            item = self.find_by_name(name)
        except:
            return {"Message": "An error occurred while inserting the item."}, 500 # internal server error

        if item:
            return item
        return {'Message': 'Item Not Found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400  # 400 is bad request
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"Message": "An error occurred while inserting the item."}, 500  # internal server error
        return item, 201  # https status code 201 for created

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}, 200
        return {'message': 'Not Found'}, 404

    def put(self, name):    # will create or update item
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        new_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(new_item)
            except:
                return {"Message": "An error occurred while inserting the item."}, 500
        else:
            try:
                self.update(new_item)
            except:
                return {"Message": "An error occurred while inserting the item."}, 500
        return new_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'items': items}

