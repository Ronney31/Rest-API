from werkzeug.security import safe_str_cmp  # to compare string
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):  # to compare string
        return user


def identity(payload):      # payload is the contents of the JWT Token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
