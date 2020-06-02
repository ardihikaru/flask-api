from app import api
from .auth.auth import api as auth_api
from .user.user import api as user_api

api.add_namespace(auth_api)
api.add_namespace(user_api)
