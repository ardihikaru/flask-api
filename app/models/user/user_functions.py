from app import app, rc
from sqlalchemy.orm.exc import NoResultFound
from app.addons.redis.translator import redis_get, redis_set
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, get_jti
from app.addons.utils import sqlresp_to_dict


def get_all_users(ses, user_model):
    try:
        data = ses.query(user_model).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def get_user_by_username(ses, user_model, username, show_passwd=False):
    try:
        data = ses.query(user_model).filter_by(username=username).one()
    except NoResultFound:
        return False, None
    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def del_user_by_username(ses, user_model, username, show_passwd=False):
    try:
        data = ses.query(user_model).filter_by(username=username).one()
        ses.query(user_model).filter_by(username=username).delete()
    except NoResultFound:
        return False, None, "User not found"

    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user, None
    else:
        return False, None, None


def store_jwt_data(json_data):
    my_identity = {
        "username": json_data["username"]
    }

    access_token = create_access_token(identity=my_identity)
    refresh_token = create_refresh_token(identity=my_identity)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)

    redis_set(rc, access_jti, False, app.config["LIMIT_ACCESS_TOKEN"])
    redis_set(rc, refresh_jti, False, app.config["LIMIT_REFRESH_TOKEN"])

    access_token_expired = decode_token(access_token)["exp"]
    refresh_token_expired = decode_token(refresh_token)["exp"]

    # redis_set(rc, json_data["username"] + "-access-token-exp", False, app.config["LIMIT_ACCESS_TOKEN"])
    # redis_set(rc, json_data["username"] + "-refresh-token-exp", False, app.config["LIMIT_REFRESH_TOKEN"])

    return access_token, refresh_token, access_token_expired, refresh_token_expired
