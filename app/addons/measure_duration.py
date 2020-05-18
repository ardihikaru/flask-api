import time
from app import info_logger
from app.addons.printer import Printer

class MeasureDuration:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        elapsed_time = self.duration()
        info_logger.logger().info("Total time taken: %s" % elapsed_time)
        Printer().cprint("Total time taken: %s" % elapsed_time)

    def duration(self):
        diff = (self.end - self.start) * 1000
        return str(round(diff, 4)) + ' milliseconds'