from app import app
from app.controllers import api
from .home.home import bp_web

app.register_blueprint(bp_web)