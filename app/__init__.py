from flask import Flask, Blueprint, url_for
from .config import Config, ProductionConfig
from .local_settings import local_settings
from .logger import err_logger, info_logger, any_logger
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_cors import CORS
from cryptography.fernet import Fernet
import os
from werkzeug.contrib.fixers import ProxyFix # Source: https://stackoverflow.com/questions/51292579/no-spec-provided-error-when-trying-to-deliver-swagger-json-over-https
from .initialization import init_folders, is_localhost
from concurrent.futures import ThreadPoolExecutor # https://gist.github.com/arshpreetsingh/006f4fafc7e20e94ad5be99b830a08c7
from flask_redis import FlaskRedis
from redis import StrictRedis

executor = ThreadPoolExecutor(100)
init_folders(local_settings)

app = Flask(__name__, static_folder = 'static', static_url_path='')
if is_localhost():
    app.config.from_object(Config)
else:
    app.config.from_object(ProductionConfig)
app.wsgi_app = ProxyFix(app.wsgi_app)

jwt     = JWTManager(app)
cors    = CORS(app, resources={r"/api/*": {"origins": "*"}})
# rc      = FlaskRedis(app)

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

rc_streamer = StrictRedis(
        host=app.config["REDIS_HOST"],
        port=int(app.config["REDIS_PORT"]),
        password=app.config["REDIS_PASSWORD"],
        db=2,
        decode_responses=True
)

rc_live_stream = StrictRedis(
        host=app.config["REDIS_HOST"],
        port=int(app.config["REDIS_PORT"]),
        password=app.config["REDIS_PASSWORD"],
        db=3,
        decode_responses=True
)

# print(" all keys rc = ", rc.keys())
# print(" all keys users = ", rc_user.keys())
# for key in rc_user.keys():
#     rc_user.delete(key)
# print(" all keys users = ", rc_user.keys())

# print(" all keys streamers = ", rc_streamer.keys())
# for key in rc_streamer.keys():
#     rc_streamer.delete(key)
# print(" all keys streamers = ", rc_streamer.keys())

# print(" all keys rc_live_stream = ", rc_live_stream.keys())

# encrypt & decrypt
key     = local_settings["android_key"].encode()
fernet  = Fernet(key)

if os.environ.get('HTTPS'):
    class MyApi(Api):
        @Property
        def specs_url(self):
            '''Monkey patch for HTTPS'''
            # return url_for(self.endpoint('specs'), _external=True, _scheme='https')
            # print("self.base_url = ", self.base_url)
            scheme = 'http' if '5000' in self.base_url else 'https'
            return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)
else:
    class MyApi(Api):
        pass

authorizations = {
    'Bearer Auth': {
        'type'  : 'apiKey',
        'in'    : 'header',
        'name'  : 'Authorization'
    }
}
# bp_api_v2 = Blueprint('api', __name__, url_prefix='/api/v2')
bp_api_v2 = Blueprint('api', __name__, url_prefix='/api')

api = MyApi(app, version='1.0', title='Flask API with Swagger UI',
        description='Web Service (APIs) GUI-based Documentation',
        doc='/api/doc/',
        # doc=False,
        prefix='/api',
        security='Bearer Auth',
        authorizations=authorizations
)

# from .queue_manager import QueueManager
# QueueManager().run()

