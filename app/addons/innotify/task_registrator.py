import os
from inotify_simple import INotify, flags
from app.addons.printer import Printer
from app.addons.api.queue.queue import Queue
import simplejson as json

class TaskRegistrator(Queue):
    def __init__(self, pool_name):
        self.set_queue_config()
        self.__set_config(pool_name)

    def __set_config(self, pool_name):
        self.data = None
        self.queue_pool_dir = self.main_path + pool_name
        self.inotify = INotify()
        # watch_flags = flags.CREATE
        watch_flags = flags.CREATE | flags.MODIFY
        self.inotify.add_watch(self.queue_pool_dir, watch_flags)
        os.chdir(self.queue_pool_dir)

    def __extract_json(self, data):
        arr_data_raw = data.split(".")
        print(" ** arr_data_raw = ", arr_data_raw)
        arr_data = arr_data_raw[0].split("-")
        print(" ** arr_data = ", arr_data)
        return arr_data[0], arr_data[1]

    def run(self, pool_name):
        event = self.inotify.read()[0]
        file_path = ""
        print(" >>>>> event = ", event)
        for flag in flags.from_mask(event.mask):
            if str(flag) == "flags.CREATE" or str(flag) == "flags.MODIFY":
                try:
                    Printer().cprint(" **** TaskRegistrator detected a new task to be registered ... name = %s" % event.name)
                    cmd, key = self.__extract_json(event.name)
                    file_path = self.main_path + pool_name + "/" + event.name
                    print(" ** DIBACA = ", file_path)
                    with open(file_path) as json_file:
                        self.data = {
                            "cmd": cmd,
                            "key": key,
                            "pool_name": pool_name,
                            "path": file_path,
                            "value": json.load(json_file)
                        }
                    print("Data .. DISIMPAN")
                    return True
                except:
                    print(" damn .. masuk else ...")
                    pass
        if os.path.exists(file_path):
            print(" sampah! deleting ..")
            os.remove(file_path)
            print(" File is deleted ..")
        return True
        # return False

    def get_data(self):
        return self.data

