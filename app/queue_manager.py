from app import app, err_logger
from app.addons.async_handler import AsyncHandler
from app.addons.innotify.common_execution import threaded_task_scheduler
from app.addons.printer import Printer
import os
from app.addons.api.queue.queue import Queue

class QueueManager(AsyncHandler, Queue):
    def __init__(self):
        super().__init__()
        self.__make_queue_dirs()

    def __make_queue_dirs(self):
        self.set_queue_config()
        for i in range(0, self.pool_size):
            if i < 10:
                idx = "0" + str(i)
            else:
                idx = str(i)
            queue_dir = self.main_path + self.prefix + idx
            if not os.path.isdir(queue_dir):
                os.makedirs(queue_dir)

    def setup_async_reader(self):
        for pool_name in self.get_queue_dir():
            Printer().cprint("spawning thread @ TaskScheduler-%s ..." % pool_name)
            try:
                kwargs = {
                    "pool_name": pool_name
                }
                self.spawn_thread(threaded_task_scheduler, kwargs)
            except:
                Printer().cprint("Somehow we unable to Start the Thread of TaskScheduler")
                err_logger.logger().error("Somehow we unable to Start the Thread of TaskScheduler")
                return False
        return True

    def run(self):
        if self.setup_async_reader():
            Printer().cprint("QueueManager [Thread handler] is running now ...")
