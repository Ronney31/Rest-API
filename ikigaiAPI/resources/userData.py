from flask_restful import Resource, reqparse
from flask import jsonify
from resources.database import databaseModel

class uData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q1', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('q2', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('q3', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('q4', type=str, required=True, help="This field cannot be left blank!")

    def get(self, userName):
        # if userName in ddata:
        userDetails = databaseModel.find_by_username(userName)
        if userDetails:
            return {"User Details ": databaseModel.json(userDetails)}, 200  # successfully found
        else:
            return {"message": "user not found."}, 400  # 400 for not found

    # enter new data if not exist
    def post(self, userName):
        # if userName in ddata:
        if databaseModel.find_by_username(userName):
            return {'Message': "User with name '{}' already exists.".format(userName)}, 400  # 400 is bad request

        data = uData.parser.parse_args()
        databaseModel.insert_data(userName, data)
        return {"Message ": "User data entered successfully."}, 201  # 201 is for created

    # enter new data and if exist override previous data
    def put(self, userName):
        data = uData.parser.parse_args()
        if databaseModel.find_by_username(userName) is None:
            try:
                databaseModel.insert_data(userName, data)
                return {"Message ": "new user added successfully."}
            except:
                return {"Message": "An error occurred while inserting the item."}, 500
        else:
            try:
                databaseModel.update_data(userName, data)
                return {"Message ": "Successfully updated existing user."}
            except Exception as e:
                # return {"Message": "An error occurred while inserting the item."e}, 500
                return {"Message": str(e)}, 500

    def delete(self, userName):
        return databaseModel.delete_user(userName)


class allUserData(Resource):
    def get(self):
        return {"users ": databaseModel.select_all()}


















'''
    # https://medium.com/thrive-global/ikigai-the-japanese-secret-to-a-long-and-happy-life-might-just-help-you-live-a-more-fulfilling-9871d01992b7
    
    What you love (your passion)
    What the world needs (your mission)
    What you are good at (your vocation)
    What you can get paid for (your profession)
'''