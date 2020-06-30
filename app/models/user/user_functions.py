from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.redis.translator import redis_get, redis_set
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, get_jti
from app.addons.utils import sqlresp_to_dict
from app.addons.cryptography.fernet import encrypt


def insert_new_data(ses, user_model, new_data):
    new_data["identifier"] = encrypt(new_data["username"])
    ses.add(user_model(
                name=new_data["name"],
                username=new_data["username"],
                email=new_data["email"],
                password=new_data["password"],
                identifier=new_data["identifier"]
            )
    )

    _, inserted_data = get_data_by_identifier(ses, user_model, new_data["identifier"])

    if len(inserted_data) > 0:
        return True, inserted_data
    else:
        return False, None


def get_data_by_identifier(ses, user_model, identifier, show_passwd=False):
    try:
        data = ses.query(user_model).filter_by(identifier=identifier).one()
    except NoResultFound:
        return False, None
    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def get_all_users(ses, user_model, args=None):
    try:
        if args is not None:
            if len(args["range"]) == 0:
                args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        else:
            args = {
                "filter": {},
                "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
                "sort": []
            }
        data_all = ses.query(user_model).all()
        data = ses.query(user_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None, 0
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict, len(data_all)
    else:
        return False, None, 0


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

def del_user_by_userid(ses, user_model, userid, show_passwd=False):
    try:
        data = ses.query(user_model).filter_by(id=userid).one()
        ses.query(user_model).filter_by(id=userid).delete()
    except NoResultFound:
        return False, None, "User not found"

    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user, None
    else:
        return False, None, None


def upd_user_by_userid(ses, user_model, userid, show_passwd=False, new_data=None):
    try:
        data = ses.query(user_model).filter_by(id=userid).one()

        if new_data is not None:
            data.name = new_data["name"] if "name" in new_data else data.name
            data.username = new_data["username"] if "username" in new_data else data.username
            data.email = new_data["email"] if "email" in new_data else data.email

        ses.query(user_model).filter_by(id=userid).update(
            {
                "name": data.name,
                "username": data.username,
                "email": data.email
            }
        )
    except NoResultFound:
        return False, None, None
    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user, None
    else:
        return False, None, None


def get_user_by_userid(ses, user_model, userid, show_passwd=False):
    try:
        data = ses.query(user_model).filter_by(id=userid).one()
    except NoResultFound:
        return False, None
    dict_user = data.to_dict(show_passwd)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


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
