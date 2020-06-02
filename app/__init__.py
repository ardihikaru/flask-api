from flask import Flask, Blueprint, url_for
from .config import Config, ProductionConfig
from .local_settings import local_settings
from .logger import err_logger, info_logger, any_logger
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_cors import CORS
from cryptography.fernet import Fernet
from werkzeug.contrib.fixers import ProxyFix
from .initialization import init_folders, is_localhost
from concurrent.futures import ThreadPoolExecutor
from flask_redis import FlaskRedis
from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager

executor = ThreadPoolExecutor(100)
init_folders(local_settings)

app = Flask(__name__, static_folder='static', static_url_path='')
if is_localhost():
    app.config.from_object(Config)
else:
    app.config.from_object(ProductionConfig)
app.wsgi_app = ProxyFix(app.wsgi_app)

Base = declarative_base()

if app.config["SECURE_CLUSTER"]:
    connect_args = {
        'sslmode': 'require',
        'sslrootcert': app.config["SSL_ROOT_CERT"],
        'sslkey': app.config["SSL_KEY"],
        'sslcert': app.config["SSL_CERT"]
    }
else:
    connect_args = {'sslmode': 'disable'}

engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"],
    connect_args=connect_args,
    echo=True  # Log SQL queries to stdout
)

from app import models
Base.metadata.create_all(engine)

jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


class DecodedRedis(StrictRedis):
    @classmethod
    def from_url(cls, url, db=None, **kwargs):
        kwargs['decode_responses'] = True
        kwargs['password'] = app.config["REDIS_PASSWORD"]
        return StrictRedis.from_url(url, db, **kwargs)


rc = FlaskRedis.from_custom_provider(DecodedRedis, app)

rc_user = StrictRedis(
    host=app.config["REDIS_HOST"],
    port=int(app.config["REDIS_PORT"]),
    password=app.config["REDIS_PASSWORD"],
    db=1,
    decode_responses=True
)

# encrypt & decrypt
key = local_settings["android_key"].encode()
fernet = Fernet(key)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
bp_api_v2 = Blueprint('api', __name__, url_prefix='/api')

api = Api(app, version='1.0', title='Flask API with Swagger UI',
          description='Web Service (APIs) GUI-based Documentation',
          doc='/api/doc/',
          # doc=False,
          prefix='/api',
          security='Bearer Auth',
          authorizations=authorizations
          )

# migrate = Migrate(app, db)  # https://flask-migrate.readthedocs.io/en/latest/
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
