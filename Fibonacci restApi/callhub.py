from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def fab_function(number):
    number = int(number)
    if number < 0:
        raise IOError
    elif number == 0:
        return 0
    a = 0
    b = 1
    for _ in range(number - 1):
        t = a + b
        a,b = b, t
    return b


class application(Resource):
    def get(self, number):
        try:
            b = fab_function(number)
            return {"Result ":b}, 200
        except Exception as e:
            return {"message": "invalid input"}, 400


api.add_resource(application, '/fab/<number>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
