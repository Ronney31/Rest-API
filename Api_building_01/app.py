'''
    this is my very first api application, to test api, i am using "insomnia".
    Rest is designed to be state less and for application to interact with things called "Resources"
'''
from flask import Flask, jsonify, request

app = Flask(__name__)

Stores = [
    {
        'name': 'My Wonderful Stores',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

'''
#request to understand
#decurator
@app.route('/') #act as homepage
def home():
    return "Hello Abyetian"
'''

# POST - used to receive data
# GET - used to send data back only

''' end point for this project'''


# POST /store data: {name:}                         = create new store with the given name
# GET /store/<string:name>                          = get a store for a given name and return some data about it
# GET /store                                        = return the list of all the store
# POST/store/<string:name>/item {name:,price:}      = it will create an item inside that specific store
# GET /store/<string:name>/item                     = get all the item in the specific store


# POST /store data: {name:}                         = create new store with the given name
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    Stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>                          = get a store for a given name and return some data about it
@app.route('/store/<string:name>')  # 'https://127.0.0.1:5000/store/someName'
def get_store(name):
    for store in Stores:
        if name == store["name"]:
            return jsonify(store)
    return jsonify({"message": "404, STORE NOT FOUND"})


# GET /store                                        = return the list of all the store
@app.route('/store')
def get_all_stores():
    return jsonify({'Stores': Stores})  # return the json ( jsonify needs dict as a parameter


# POST  /store/<string:name>/item {name:,price:}      = it will create an item inside that specific store
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in Stores:
        if name == store["name"]:
            new_items = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_items)
            return jsonify({"store": store})
    return jsonify({"message": "404, STORE NOT FOUND"})


# GET /store/<string:name>/item                     = get all the item in the specific store
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item_from_store(name):
    for store in Stores:
        if name == store["name"]:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "404, STORE NOT FOUND"})


# to start the app
app.run(port=5000)
