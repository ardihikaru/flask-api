from app import app, rc, local_settings, rc_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.addons.utils import (
    get_json_template
)
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, get_jti
from app.addons.database_blacklist.blacklist_helpers import (
    revoke_current_token, extract_identity
)
from app.addons.redis.translator import redis_get, redis_set
from app.addons.storage.storage import MyStorage
from app.addons.utils import get_today, load_file, str_to_date, date_to_str, diff_dates_in_hours
from app.models.user.user_model import UserModel
import simplejson as json
from datetime import datetime

class User():

    def to_dict(self):
        return None

    def insert(self, data):
        username = data["username"]
        existed_user = redis_get(rc_user, username)
        if existed_user is not None: # cukup update last_login
            existed_user["last_login"] = get_today()
            redis_set(rc_user, username, existed_user)
        else: # new user
            data["email"] = data["username"]
            data["last_login"] = get_today()
            data.pop("android_key", None)
            data = UserModel(data).get_user_model()
            redis_set(rc_user, username, data)

    def update(self, ikey, new_data):
        old_data = redis_get(rc_user, ikey)
        updated_data = old_data
        for key in old_data:
            if key in new_data:
                if key == "played_games" and len(new_data[key]) > 0:
                    for idx, played_game in enumerate(new_data[key]):
                        new_data[key][idx] = played_game.upper()
                updated_data[key] = new_data[key]
        redis_set(rc_user, ikey, updated_data)
        return updated_data

    def delete(self, username):
        rc_user.delete(username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def revokesExistedToken(self, encoded_token=None):
        if encoded_token:
            revoke_current_token(encoded_token, {"revoke": True})

    def doLogout(self, encoded_token=None):
        my_identity = extract_identity(encoded_token)
        MyStorage().logging_logout(my_identity["username"])
        self.revokesExistedToken(encoded_token)
        return get_json_template(response=True, results=-1, total=-1, message="Logout Success.")

    def do_refresh_token(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        access_jti = get_jti(encoded_token=access_token)
        redis_set(rc, access_jti, False, app.config["LIMIT_ACCESS_TOKEN"])
        decoded_token = decode_token(access_token)
        resp_data = {
            'access_token': access_token,
            'access_token_expired': decoded_token["exp"]
        }
        resp = get_json_template(response=True, results=resp_data, message="New access_token has been generated", total=-1)
        return resp

    def __extract_json_inputs(self, json_data):
        if json_data:
            if "login_by" not in json_data:
                return False, None, "Which OAuth2 did you use to login?"
            if "username" not in json_data:
                return False, None, "Unable to extract 'Username'."
            if "android_key" not in json_data:
                return False, None, "Unable to extract 'Username'."
            if json_data["android_key"] != local_settings["android_key"]:
                return False, None, "Android Key is INVALID."
        return True, json_data, None

    def validate_user(self, json_data):
        is_valid, json_data, msg = self.__extract_json_inputs(json_data)

        if not is_valid:
            return get_json_template(response=is_valid,
                                     message=msg)

        self.insert(json_data)

        my_identity = {
            "username": json_data["username"],
            "default_user_type": redis_get(rc_user, json_data["username"])["default_user_type"]
        }

        access_token = create_access_token(identity=my_identity)
        refresh_token = create_refresh_token(identity=my_identity)

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)

        redis_set(rc, access_jti, False, app.config["LIMIT_ACCESS_TOKEN"])
        redis_set(rc, refresh_jti, False, app.config["LIMIT_REFRESH_TOKEN"])

        access_token_expired = decode_token(access_token)["exp"]
        refresh_token_expired = decode_token(refresh_token)["exp"]

        results = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expired": access_token_expired,
            "refresh_token_expired": refresh_token_expired,
        }
        MyStorage().logging_login(json_data["username"])

        return get_json_template(True, results, -1, "Login Success.")

    def __get_by_username(self, username):
        return redis_get(rc_user, username)

    def get_user(self, encoded_token, iusername):
        username = extract_identity(encoded_token)["username"]
        if iusername == "all":
            users = []
            for username in rc_user.keys():
                user = self.__get_by_username(username)
                users.append(user)
            return get_json_template(response=True, results=users, total=len(users), message="Users have been collected.")
        else:
            user = self.__get_by_username(username) if iusername == "me" else self.__get_by_username(iusername)
            msg = "User found." if user is not None else "User NOT FOUND."
            return get_json_template(response=True, results=user, total=-1, message=msg)

    def __is_admin(self, username):
        admins = [
            "ardihikaru3@gmail.com",
            "fahim.bagar@gmail.com"
        ]
        if username in admins:
            return True
        else:
            return False

    def deleting_user(self, encoded_token, target_username):
        logged_username = extract_identity(encoded_token)["username"]
        existed_user = redis_get(rc_user, target_username)
        if existed_user is None:
            return get_json_template(response=False, results=None, total=-1,
                                     message="User not Found.")

        if self.__is_admin(logged_username):
            self.delete(target_username)
            result = {"deleted_username": target_username}
            return get_json_template(response=True, results=result, total=-1, message="Username [%s] has been deleted." % target_username)
        else:
            return get_json_template(response=False, results=None, total=-1, message="You do not have access to this feature.")

    def updating_user(self, encoded_token, new_data):
        logged_username = extract_identity(encoded_token)["username"]
        updated_data = self.update(logged_username, new_data)
        return get_json_template(response=True, results=updated_data, total=-1,
                                 message="You information has been updated.")

    def __get_last_login(self, binary_id):
        log_login_dir = local_settings["logging_login_path"]
        last_login = None
        log_path = log_login_dir + binary_id + ".json"
        try:
            data = load_file(log_path)
            last_login = json.loads(data)["last_login"]
        except:
            pass
        return last_login

    def __get_is_logout(self, username):
        log_login_dir = local_settings["logging_login_path"]
        is_login = True
        log_path = log_login_dir + username + ".json"
        try:
            data = load_file(log_path)
            is_login = json.loads(data)["is_login"]
        except:
            pass
        return is_login

    def __is_user_active(self, username):
        last_login = self.__get_last_login(username)
        if last_login is None:
            return False
        is_login        = self.__get_is_logout(username)
        date_format     = "%Y-%m-%d %H:%M:%S"
        date_now        = str_to_date(date_to_str(datetime.now(), date_format), date_format)
        date_old        = str_to_date(last_login, date_format)
        diff_hours      = diff_dates_in_hours(date_now, date_old)

        if is_login and diff_hours < app.config["LOGIN_ACTIVE"]:
            return True
        return False

    def get_active_users(self):
        active_users = []
        for username in rc_user.keys():
            user = redis_get(rc_user, username)
            if self.__is_user_active(username):
                active_users.append(user)
        return get_json_template(response=True, results=active_users, total=len(active_users),
                                 message="Active users have been collected.")

    def get_played_games(self, encoded_token=None, username=None):
        if encoded_token is not None:
            logged_username = extract_identity(encoded_token)["username"]
            played_games = redis_get(rc_user, logged_username)["played_games"]
            return get_json_template(response=True, results=played_games, total=len(played_games),
                                     message="Data have been collected.")
        elif username is not None:
            played_games = redis_get(rc_user, username)["played_games"]
            return get_json_template(response=True, results=played_games, total=len(played_games),
                                     message="Data have been collected.")
        else:
            return get_json_template(response=False, results=None, total=0,
                                     message="BAD REQUEST")

    def get_gamer_of(self, game_title):
        game_title = game_title.upper().replace('-', ' ')
        list_of_users = []
        for username in rc_user.keys():
            user = redis_get(rc_user, username)
            played_games = user["played_games"]
            if game_title in played_games:
                list_of_users.append(user)

        return get_json_template(response=True, results=list_of_users, total=len(list_of_users),
                                 message="Gamer of [%s] has been collected."  % game_title)

    def get_favorite(self, encoded_token=None, username=None):
        if encoded_token is not None:
            logged_username = extract_identity(encoded_token)["username"]
            favorites = redis_get(rc_user, logged_username)["favorites"]
            return get_json_template(response=True, results=favorites, total=len(favorites),
                                     message="Favorite Data have been collected.")
        elif username is not None:
            favorites = redis_get(rc_user, username)["favorites"]
            return get_json_template(response=True, results=favorites, total=len(favorites),
                                     message="Favorite Data have been collected.")
        else:
            return get_json_template(response=False, results=None, total=0,
                                     message="BAD REQUEST")

    def get_followed_streamer(self, streamer_id):
        list_of_users = []
        for username in rc_user.keys():
            user = redis_get(rc_user, username)
            favorites = user["favorites"]
            if streamer_id in favorites:
                list_of_users.append(user)

        return get_json_template(response=True, results=list_of_users, total=len(list_of_users),
                                 message="Followers has been collected.")
