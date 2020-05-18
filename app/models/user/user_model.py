
class UserModel():
    def __init__(self, initial_data):
        self.user_model = initial_data
        self.__set_default_keys()
        self.set_user_model()

    def set_user_model(self):
        for key in self.default_keys:
            self.user_model[key] = self.get_value(key)

    def get_user_model(self):
        return self.user_model

    def __set_default_keys(self):
        self.default_keys = [
            "default_user_type",
            "profile",
            "accounts",
            "user_type",
            "played_games",
            "favorites"
        ]

    def list_of_user_types(self):
        return [
            "user",
            "streamer",
            "seller"
        ]

    def get_value(self, type):
        if type == "default_user_type":
            return "user"
        elif type == "profile":
            return self.get_profile_model()
        elif type == "accounts":
            return self.get_account_model()
        elif type == "user_type":
            return self.get_user_type_model()
        elif type == "played_games":
            return self.get_played_games_model()
        elif type == "favorites":
            return self.get_favorite_model()

    def get_profile_model(self):
        return {
            "fullname": None,
            "gender": None,
            "city": None
        }

    def get_account_model(self):
        account_model = {
            "gmail" : {"is_login": False},
            "youtube" : {"is_login": False},
            "facebook" : {"is_login": False},
        }
        account_model[self.user_model["login_by"]]["is_login"] = True
        self.user_model.pop("login_by", None)
        return account_model

    def get_user_type_model(self):
        return {
            "streamer" : {
                "streamer_id": None,
                "streaming_history": [],
            },
            "seller" : {
                "streamer_id": None,
                "streaming_history": [],
            }
        }

    def get_played_games_model(self):
        return []

    def get_favorite_model(self):
        return []