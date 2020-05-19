from app import app, engine, local_settings, Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from app.addons.utils import sql_to_dict_resp, get_json_template, jsonifyResultV2, setQueryLimit, setQueryOptWhere, \
    sqlresp_to_dict
from app.addons.database_blacklist.blacklist_helpers import (
    revoke_current_token
)
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from .user_model import UserModel
from .user_functions import get_user_by_username


class User(UserModel):
    def __init__(self):
        self.resp_status = None
        self.resp_data = None
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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def doLogout(self):
        session.clear()
        return get_json_template(response=True, results=-1, total=-1, message="Logout Success.")

    def __validate_register_data(self, ses, json_data):
        if "name" not in json_data:
            return False, "Name should not be EMPTY."

        if "username" not in json_data:
            return False, "Username should not be EMPTY."

        if "password" not in json_data:
            return False, "Password should not be EMPTY."

        if "password_confirm" not in json_data:
            return False, "Password Confirmation is EMPTY."

        if json_data["password"] != json_data["password_confirm"]:
            return False, "Password Confirmation missmatch with Password."

        is_id_exist, _ = get_user_by_username(ses, User, json_data["username"])
        if is_id_exist:
            return False, "Username `%s` have been used." % json_data["username"]

        return True, None

    def tranc_register(self, ses, json_data):
        is_valid, msg = self.__validate_register_data(ses, json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registration is success. Now, you can login into our system."
            self.set_password(json_data["password"])
            json_data["password"] = self.password_hash
            # self.insert(ses, json_data)
            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.tranc_register(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
