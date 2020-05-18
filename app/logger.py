import logging
import os

class Logger():
    def __init__(self, logger_fname, logger_level="DEBUG", is_clean=False):
        self.is_clean = is_clean
        self.set_logger_file(logger_fname)
        self.set_logger_level(logger_level)
        self.set_log_format()

    def get_logger_file(self):
        return self.logger_file

    def set_logger_file(self, logger_fname):
        logger_dir      = "app/data/resources/logs/"

        if not os.path.exists(logger_dir):
            os.makedirs(logger_dir)

        self.logger_name = logger_dir + logger_fname
        self.logger_file = logger_dir + logger_fname + '.log'

    def set_log_format(self):
        if self.is_clean:
            self.formatter = logging.Formatter('%(message)s') 
        else:
            self.formatter = logging.Formatter('%(levelname)s %(asctime)s { module name : %(module)s Line no : %(lineno)d} %(message)s')
        
    def set_logger_level(self, logger_level):
        if logger_level == "DEBUG":
            self.logger_level = logging.DEBUG
        elif logger_level == "INFO":
            self.logger_level = logging.INFO
        elif logger_level == "WARN":
            self.logger_level = logging.WARN
        elif logger_level == "ERROR":
            self.logger_level = logging.ERROR
        elif logger_level == "FATAL":
            self.logger_level = logging.FATAL
        else:
            self.logger_level = None

    def logger(self):
        """Function setup as many loggers as you want"""
        handler = logging.FileHandler(self.logger_file)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_level)
        logger.addHandler(handler)

        return logger

err_logger      = Logger("error", "ERROR")
info_logger     = Logger("info", "INFO")
any_logger      = Logger("binary", "INFO", True)
