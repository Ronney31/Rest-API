from werkzeug.security import safe_str_cmp  # to compare string
from user import User

# users = [
#     {
#         'id' : 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# ]

# username_mapping = {'bob': {
#         'id' : 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }

# userid_mapping = {1: {
#         'id' : 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)     # None is a default value
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):  # to compare string
        return user


def identity(payload):      # payload is the contents of the JWT Token
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
