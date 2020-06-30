from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.redis.translator import redis_get, redis_set
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, get_jti
from app.addons.utils import sqlresp_to_dict
from app.addons.cryptography.fernet import encrypt
# from datetime import date  # eg.g date.today())
from sqlalchemy import Date, cast, and_  # detailed here: https://docs.sqlalchemy.org/en/13/core/sqlelement.html?


def insert_new_data(ses, user_model, new_data):
    new_data["identifier"] = encrypt(new_data["username"])
    if "create_time" in new_data:
        ses.add(user_model(
            name=new_data["name"],
            username=new_data["username"],
            email=new_data["email"],
            hobby=new_data["hobby"],
            password=new_data["password"],
            identifier=new_data["identifier"],
            create_time=new_data["create_time"]
        ))
    else:
        ses.add(user_model(
            name=new_data["name"],
            username=new_data["username"],
            email=new_data["email"],
            hobby=new_data["hobby"],
            password=new_data["password"],
            identifier=new_data["identifier"]
        ))

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
            data.hobby = new_data["hobby"] if "hobby" in new_data else data.hobby

        ses.query(user_model).filter_by(id=userid).update(
            {
                "name": data.name,
                "username": data.username,
                "email": data.email,
                "hobby": data.hobby
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


def get_user_data_by_hobby(ses, user_model, hobby, register_after):
    try:
        data = ses.query(user_model).filter_by(hobby=hobby).filter(cast(user_model.create_time, Date) >= register_after).all()
    except NoResultFound:
        return False, None
    dict_user = sqlresp_to_dict(data)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def get_user_data_by_hobby_between(ses, user_model, hobby, start_date, end_date):
    try:
        data = ses.query(user_model).filter_by(hobby=hobby).filter(
            and_(
                cast(user_model.create_time, Date) >= start_date,
                cast(user_model.create_time, Date) <= end_date
            )
        ).all()
    except NoResultFound:
        return False, None
    dict_user = sqlresp_to_dict(data)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def del_all_data(ses, data_model, args=None):
    deleted_data = []
    no_filter = True
    try:
        data = None
        if len(args["filter"]) > 0:
            if "id" in args["filter"]:
                for i in range(len(args["filter"]["id"])):
                    uid = args["filter"]["id"][i]
                    data = ses.query(data_model).filter_by(id=uid).one()
                    deleted_data.append(data.to_dict())
                    ses.query(data_model).filter_by(id=uid).delete()
                    no_filter = False
        if no_filter:
            data = ses.query(data_model).all()
            ses.query(data_model).delete()
    except NoResultFound:
        return False, None, "User not found"

    if no_filter:
        dict_drone = sqlresp_to_dict(data)
    else:
        dict_drone = deleted_data

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None

