from app.addons.utils import get_today, get_var_datatype

class StreamerModel():
    def __init__(self):
        self.__set_streamer_model()
        self.__set_model_type()
        self.is_verified = True
        self.msg = "OK"

    def __set_streamer_model(self):
        self.streamer_model = {
            "stream_source": None,
            "username": None,
            "account_url": None,
            "is_streaming": False,
            "last_streaming": None,
            "played_games": [],
            "added_at": get_today()
        }
        self.optional_keys = ["username", "is_streaming", "last_streaming", "played_games", "added_at"]

    def __set_model_type(self):
        self.model_type = {
            "stream_source": "str",
            "username": "str",
            "account_url": "str",
            "is_streaming": "bool",
            "last_streaming": "str",
            "played_games": "list",
            "added_at": "str"
        }

    def set_input_model(self, input_model):
        self.input_model = input_model
        self.__verify_input()

    def __is_key_verified(self, key):
        try:
            if get_var_datatype(self.model_type[key]) == get_var_datatype(self.input_model[key]):
                return True
            else:
                return False
        except:
            return False

    def __set_username(self):
        if self.is_verified and self.input_model["account_url"][-1:] == "/":
            username = self.input_model["account_url"][:-1].split('/')[-1]
        else:
            username = self.input_model["account_url"].split('/')[-1]
        self.input_model["username"] = username

    def __verify_input(self):
        for key in self.streamer_model:
            if key not in self.input_model and key not in self.optional_keys:
                self.is_verified = False
                self.msg = "Unable to extract [%s]." % key
                break
            elif not self.__is_key_verified(key) and key not in self.optional_keys:
                self.is_verified = False
                self.msg = "[%s] must be '%s'" % (key, get_var_datatype(self.model_type[key]))
                break
        for key in self.streamer_model:
            if key not in self.input_model:
                self.input_model[key] = self.streamer_model[key]
        self.__set_username()

    def get_input_model(self):
        return self.is_verified, self.input_model, self.msg
