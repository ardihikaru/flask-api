from app.addons.api.queue.queue import Queue
import os

class TaskExecutor(Queue):
    def __init__(self):
        self.set_queue_config()

    def execute_task(self, data):
        print(data)
        # file_path = data["path"]
        if data["cmd"] == "UC":
            print("Registering new user")
            print(" ##### executing the task into redis --- key = ", data["key"])
        elif data["cmd"] == "UD":
            print("Deleting new user")
        elif data["cmd"] == "UE":
            print("Editing new user")

        print(" Begin Deleting executed file ...")
        os.remove(data["path"])
        print(" executed File is deleted ..")

