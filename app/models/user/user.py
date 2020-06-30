from app import app, engine, local_settings, Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from app.addons.utils import json_load_str, get_json_template
from app.addons.database_blacklist.blacklist_helpers import (
    revoke_current_token, extract_identity
)
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from .user_model import UserModel
from .user_functions import get_all_users, get_user_by_username, del_user_by_username, store_jwt_data, \
    del_user_by_userid, upd_user_by_userid, get_user_by_userid, insert_new_data
import simplejson as json


class User(UserModel):
    def __init__(self):
        self.resp_status = None
        self.resp_data = None
        self.total_records = 0
        self.msg = None
        self.password_hash = None

    def set_resp_status(self, status):
        self.resp_status = status

    def set_resp_data(self, json_data):
        self.resp_data = json_data

    def set_msg(self, msg):
        self.msg = msg

    def set_password(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def is_password_match(self, password):
        return check_password_hash(self.password_hash, password)

    def revokesExistedToken(self, encoded_token=None):
        if encoded_token:
            revoke_current_token(encoded_token, {"revoke": True})

    def do_logout(self, encoded_token=None):
        self.revokesExistedToken(encoded_token)
        return get_json_template(response=True, results=-1, total=-1, message="Logout Success.")

    def __validate_register_data(self, ses, json_data):
        is_input_valid = True
        if "name" not in json_data:
            return False, "Name should not be EMPTY."

        if "username" not in json_data:
            return False, "Username should not be EMPTY."

        if "email" not in json_data:
            return False, "Email should not be EMPTY."

        if "password" not in json_data:
            return False, "Password should not be EMPTY."

        if "password_confirm" not in json_data:
            return False, "Password Confirmation is EMPTY."

        if json_data["password"] != json_data["password_confirm"]:
            return False, "Password Confirmation missmatch with Password."

        if is_input_valid:
            is_id_exist, _ = get_user_by_username(ses, User, json_data["username"])
            if is_id_exist:
                return False, "Username `%s` have been used." % json_data["username"]

        return True, None

    def trx_register(self, ses, json_data):
        is_valid, msg = self.__validate_register_data(ses, json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registration is success. Now, you can login into our system."
            self.set_password(json_data["password"])
            json_data["password"] = self.password_hash
            _, json_data = insert_new_data(ses, UserModel, json_data)
            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_register(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def __validate_login_data(self, ses, json_data):
        self.set_resp_status(False)
        self.set_resp_data(json_data)
        is_input_valid = True
        if "username" not in json_data:
            is_input_valid = False
            self.set_msg("Username should not be EMPTY.")

        if "password" not in json_data:
            is_input_valid = False
            self.set_msg("Password should not be EMPTY.")

        if is_input_valid:
            is_id_exist, user_data = get_user_by_username(ses, User, json_data["username"], show_passwd=True)
            if is_id_exist:
                self.password_hash = user_data["password"]
                if self.is_password_match(json_data["password"]):  # check password
                    self.set_resp_status(is_id_exist)
                    self.set_msg("User data FOUND.")

                    access_token, refresh_token, access_token_expired, refresh_token_expired = store_jwt_data(json_data)

                    # set resp_data
                    resp_data = {"access_token": access_token,
                                 "refresh_token": refresh_token,
                                 "access_token_expired": access_token_expired,
                                 "refresh_token_expired": refresh_token_expired,
                                 "username": json_data["username"]}
                    self.set_resp_data(resp_data)
                else:
                    self.set_msg("Incorrect Password.")
            else:
                self.set_msg("Incorrect Username.")

    def validate_user(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.__validate_login_data(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_users(self, ses, get_args=None):
        is_valid, users, self.total_records = get_all_users(ses, User, get_args)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(users)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if "filter" in get_args:
                get_args["filter"] = json_load_str(get_args["filter"], "dict")
            if "range" in get_args:
                get_args["range"] = json_load_str(get_args["range"], "list")
            if "sort" in get_args:
                get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_users(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_users(var, get_args=get_args))
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg,
                                 total=self.total_records)

    def trx_get_data_by_username(self, ses, username):
        is_valid, user_data = get_user_by_username(ses, User, username)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(user_data)

    def get_data_by_username(self, username):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_username(var, username))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_username(self, ses, username):
        is_valid, user_data, msg = del_user_by_username(ses, User, username)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(user_data)

    def delete_data_by_username(self, username):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_username(var, username))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_userid(self, ses, userid):
        is_valid, user_data, msg = del_user_by_userid(ses, User, userid)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(user_data)

    def delete_data_by_userid(self, userid):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_userid(var, userid))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_upd_data_by_userid(self, ses, userid, json_data):
        is_valid, user_data, msg = upd_user_by_userid(ses, User, userid, new_data=json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Updating data success.")

        self.set_resp_data(user_data)

    def update_data_by_userid(self, userid, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_upd_data_by_userid(var, userid, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_data_by_userid(self, ses, userid):
        is_valid, user_data = get_user_by_userid(ses, User, userid)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(user_data)

    def get_data_by_userid(self, userid):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_userid(var, userid))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
