import os
from inotify_simple import INotify, flags
import simplejson as json

try:
    from app import local_settings
except:
    local_settings = {
        "inotify_config": {
            "default_dir": "/app/tick/",
            "default_name": "data.json"
        }
    }

class TickNotifierOrigin():
    def __init__(self, symbol, binary_id, id):
        self.__set_config(symbol, binary_id, id)

    def __set_config(self, symbol, binary_id, id):
        self.binary_id = binary_id
        self.id = id
        self.tick_dir = local_settings["inotify_config"]["default_dir"] + symbol
        self.tick_file_path = self.tick_dir + "/" + local_settings["inotify_config"]["default_name"]
        self.inotify = INotify()
        watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
        self.inotify.add_watch(self.tick_dir, watch_flags)
        os.chdir(self.tick_dir)
        self.tick_data = None
        self.symbol = symbol

    def run(self):
        event = self.inotify.read()[0]
        for flag in flags.from_mask(event.mask):
            if str(flag) == "flags.MODIFY":
                with open(self.tick_file_path) as json_file:
                    self.tick_data = json.load(json_file)
        return True

    def get_tick_data(self):
        return {
            "id": self.id,
            "binary_id": self.binary_id,
            "symbol": self.symbol,
            "data": self.tick_data
        }
        # return [self.id, self.binary_id, self.symbol, self.tick_data]

