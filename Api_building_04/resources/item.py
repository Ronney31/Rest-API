import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'Message': 'Item Not Found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400  # 400 is bad request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"Message": "An error occurred while inserting the item."}, 500  # internal server error
        return item.json(), 201  # https status code 201 for created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200
        return {'message': 'Not Found'}, 404

    def put(self, name):    # will create or update item
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])  # because find_by_name found nothing, so we are creating new one.
        else:
            item.price = data['price']
        item.save_to_db()  # as the item is uniquely identified by id

        return item.json()


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

