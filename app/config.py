import os
import datetime
import simplejson as json


def get_redis_url():
    root_dir = os.path.dirname(os.path.abspath(__file__)).replace("app", "")
    redis_url_path = root_dir + "url_host.json"
    with open(redis_url_path, 'r') as file:
        data = file.read().replace('\n', '')

    url = json.loads(data)["host"]
    domain = url.split("//")[-1].split("/")[0]
    return domain


def get_database_uri(is_secured, passwd):
    if is_secured:
        return 'cockroachdb://flaskuser:%s@localhost:26257/flaskapi' % passwd
    else:
        return 'cockroachdb://flaskuser@localhost:26257/flaskapi'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Vda6r7/3yXBHLDSd89asmN]LWX/,?RT'

    LIMIT_ACCESS_TOKEN = 30 * 24 * 60 * 60
    LIMIT_REFRESH_TOKEN = 120 * 24 * 60 * 60

    JWT_SECRET_KEY = '1n!R4h45|1Aa-bY-@rD!1'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=LIMIT_ACCESS_TOKEN)  # 1 hari = 24*60*60
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=LIMIT_REFRESH_TOKEN)  # 1 hari = 24*60*60
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True

    ENABLE_PRINTER = True
    THRES_ECRYPTED = 30  # if higher, then, it is already ENCRYPTED
    LOGIN_ACTIVE = 5  # last 5 hours
    FLASK_ENV = "development"

    SECURE_CLUSTER = False
    SQLALCHEMY_DATABASE_PASSWD = "bismillah"
    # SECURE_CLUSTER = True
    SQLALCHEMY_DATABASE_URI = get_database_uri(SECURE_CLUSTER, SQLALCHEMY_DATABASE_PASSWD)
    SSL_ROOT_CERT = 'app/certs/ca.crt'
    SSL_KEY = 'app/certs/client.flaskuser.key'
    SSL_CERT = 'app/certs/client.flaskuser.crt'

    RESTPLUS_MASK_SWAGGER = False

    REDIS_HOST = get_redis_url()
    REDIS_PORT = "6379"
    REDIS_PASSWORD = "bismillah"
    REDIS_DB_APP = "0"
    REDIS_DB_USER = "1"
    REDIS_KEY_EXPIRED = LIMIT_ACCESS_TOKEN
    REDIS_URL = "redis://:" + REDIS_PASSWORD + "@" + REDIS_HOST + ":" + REDIS_PORT + "/" + REDIS_DB_APP

    APIKEY_YOUTUBE = "AIzaSyBz03FEDwxEQyRhW9uMpOwD3g5jFMkfV8s"


class ProductionConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Vda6r7/3yXBHLDSd89asmN]LWX/,?RT'

    LIMIT_ACCESS_TOKEN = 30 * 24 * 60 * 60
    LIMIT_REFRESH_TOKEN = 120 * 24 * 60 * 60

    JWT_SECRET_KEY = '1n!R4h45|1Aa-bY-@rD!1'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=LIMIT_ACCESS_TOKEN)  # 1 hari = 24*60*60
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=LIMIT_REFRESH_TOKEN)  # 1 hari = 24*60*60
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True

    ENABLE_PRINTER = False
    THRES_ECRYPTED = 30  # if higher, then, it is already ENCRYPTED
    LOGIN_ACTIVE = 5  # last 5 hours

    SECURE_CLUSTER = False
    SQLALCHEMY_DATABASE_PASSWD = "bismillah"
    # SECURE_CLUSTER = True
    SQLALCHEMY_DATABASE_URI = get_database_uri(SECURE_CLUSTER, SQLALCHEMY_DATABASE_PASSWD)
    SSL_ROOT_CERT = 'app/certs/ca.crt'
    SSL_KEY = 'app/certs/client.flaskuser.key'
    SSL_CERT = 'app/certs/client.flaskuser.crt'

    RESTPLUS_MASK_SWAGGER = False

    REDIS_HOST = get_redis_url()
    REDIS_PORT = "6379"
    REDIS_PASSWORD = "bismillah"
    REDIS_DB_APP = "0"
    REDIS_DB_USER = "1"
    REDIS_KEY_EXPIRED = LIMIT_ACCESS_TOKEN
    REDIS_URL = "redis://:" + REDIS_PASSWORD + "@" + REDIS_HOST + ":" + REDIS_PORT + "/" + REDIS_DB_APP

    APIKEY_YOUTUBE = "AIzaSyBz03FEDwxEQyRhW9uMpOwD3g5jFMkfV8s"
