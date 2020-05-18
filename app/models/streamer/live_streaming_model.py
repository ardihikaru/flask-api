from app.addons.utils import get_today, get_var_datatype

class LiveStreamingModel():
    def __init__(self):
        self.__set_live_streaming_model()
        self.__set_model_type()
        self.is_verified = True
        self.msg = "OK"

    def __set_live_streaming_model(self):
        self.live_streaming_model = {
            "streamer_id": None,
            "streaming_time": get_today(),
            "stream_url": None
        }
        self.optional_keys = ["streaming_time"]

    def __set_model_type(self):
        self.model_type = {
            "streamer_id": "str",
            "streaming_time": "str",
            "stream_url": "str"
        }

    def set_input_model(self, streamer_id, input_model):
        self.input_model = {}
        self.input_model["streamer_id"] = streamer_id
        self.input_model["stream_url"] = input_model["stream_url"]
        self.__verify_input()

    def __is_key_verified(self, key):
        try:
            if get_var_datatype(self.model_type[key]) == get_var_datatype(self.input_model[key]):
                return True
            else:
                return False
        except:
            return False

    def __verify_input(self):
        for key in self.live_streaming_model:
            if key not in self.input_model and key not in self.optional_keys:
                self.is_verified = False
                self.msg = "Unable to extract [%s]." % key
                break
            elif not self.__is_key_verified(key) and key not in self.optional_keys:
                self.is_verified = False
                self.msg = "[%s] must be '%s'" % (key, get_var_datatype(self.model_type[key]))
                break
        for key in self.live_streaming_model:
            if key not in self.input_model:
                self.input_model[key] = self.live_streaming_model[key]

    def get_input_model(self):
        return self.is_verified, self.input_model, self.msg
