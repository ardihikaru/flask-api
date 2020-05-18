from app import executor, err_logger
import sys
# from _thread import start_new_thread
from threading import Thread

class AsyncHandler():
    def __init__(self):
        # self.type = "thread"
        self.type = "concurrent"

    def spawn_thread(self, func, kwargs_data):
        if self.type == "thread":
            # print("spawn @ thread NATIVE")
            self.spawn_native_thread(func, kwargs_data)
        elif self.type == "subprocess":
            # print("spawn @ subprocess")
            self.spawn_subprocess(func, kwargs_data)
        elif self.type == "concurrent":
            # print("spawn @ concurrent")
            self.spawn_future_concurency_thread(func, kwargs_data)
        else:
            # print("mbuh spawn opo iki")
            self.spawn_future_concurency_thread(func, kwargs_data)

    def spawn_future_concurency_thread(self, func, kwargs_data):
        try:
            executor.submit(func, **kwargs_data)
            # executor.submit(func, 1)
            # executor.submit(func, 2)
            # executor.submit(func, 3)
            # executor.submit(func, 4)
            # executor.submit(func, 5)
            return True
        except:
            e = sys.exc_info()[0]
            err_logger.logger().error(e)
            return False

    def spawn_native_thread(self, func, kwargs_data):
        # print("masuk @ THREAD sini ..")
        # start_new_thread(func(**kwargs_data))
        t = Thread(target=func(**kwargs_data))
        t.start()
        t.join()
        # print("ok @ THREAD selesai ..")
        return True

    def spawn_subprocess(self, func, kwargs_data):
        # print("masuk sini ..")
        func(**kwargs_data)
        # print("ok selesai ..")
        return True

