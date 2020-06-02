from app import app #, local_settings

class Printer():
    def __init__(self):
        self.is_enabled = app.config["ENABLE_PRINTER"]

    def cprint(self, msg):
        ''' Console-Level Printing '''
        if self.is_enabled:
            print(msg)