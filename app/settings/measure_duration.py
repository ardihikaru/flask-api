import time
from app import info_logger

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
        print("Total time taken: %s" % elapsed_time)

    def duration(self):
        # print(" >> self.start = " + str(self.start))
        # print(" >> self.enddd = " + str(self.end))
        # return str(self.end - self.start) + ' seconds'
        diff = (self.end - self.start) * 1000
        return str(round(diff, 4)) + ' milliseconds'
        # return str((self.end - self.start) * 1000000) + ' microseconds'