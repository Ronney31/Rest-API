import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"Message": "An error occurred while inserting the item."}, 500 # internal server error

        if item:
            return item.json()
        return {'Message': 'Item Not Found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400  # 400 is bad request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {"Message": "An error occurred while inserting the item."}, 500  # internal server error
        return item.json(), 201  # https status code 201 for created

    def delete(self, name):
        if ItemModel.find_by_name(name):
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
        item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, data['price'])
        if item is None:
            try:
                new_item.insert()
            except:
                return {"Message": "An error occurred while inserting the item."}, 500
        else:
            try:
                new_item.update()
            except:
                return {"Message": "An error occurred while inserting the item."}, 500
        return new_item.json()


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

