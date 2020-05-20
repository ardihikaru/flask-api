import socket, os, simplejson as json
from app.addons.printer import Printer
from time import sleep
from app import app

class UDPClient():
    def __init__(self, local_settings, watcher_path=None, file_path=None, timeout=None, binary_id=None):
        self.inits(local_settings, watcher_path, file_path, timeout, binary_id)

    def inits(self, local_settings, watcher_path, file_path, timeout, binary_id):
        url = app.config["UDP_URL"]

        port = local_settings["udp_config"]["port"]
        if binary_id is not None:
            root_dir = local_settings["udp_config"]["stored_response"] + binary_id + "/"
            error_dir = local_settings["udp_config"]["stored_response"] + "/"
            self.echo_path = root_dir + local_settings["udp_config"]["output"]["echo"] + ".json"
            self.extra_timeout = local_settings["udp_config"]["extra_timeout"]
            self.error_path = error_dir + local_settings["udp_config"]["output"]["error"] + ".json"
            self.binary_id = binary_id
        self.watcher_path = watcher_path
        self.file_path = file_path
        self.timeout = timeout # seconds

        self.set_server_addr(url, port)
        self.create_udp_socket()

    def set_server_addr(self, url, port):
        self.server_address = (url, port)

    def create_udp_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, message):
        bytes_msg = str.encode(message)
        try:
            # Printer().cprint('sending {!r}'.format(message))
            self.sock.sendto(bytes_msg, self.server_address)
        finally:
            # Printer().cprint('closing socket')
            self.sock.close()

    def __collect_udp_data(self):
        try:
            with open(self.file_path, "r") as read_file:
                jsonified_data = json.load(read_file)
            return jsonified_data
        except:
            return None

    def __deleting_on_read(self, is_echo=False):
        if is_echo:
            os.remove(self.echo_path)
        else:
            os.remove(self.file_path)

    def __is_maxhub_panic(self):
        try:
            if self.binary_id is not None and os.path.exists(self.error_path):
                return True
        except:
            return False
        return False

    def get_jsonified_data(self, is_extra_delay=False):
        tick = 1

        # if have error.json (maxhub is Panic!), then, deny it.
        if self.__is_maxhub_panic():
            return None, None

        if is_extra_delay:
            this_timeout = self.extra_timeout
        else:
            this_timeout = self.timeout

        while tick <= this_timeout:

            # again, check error.json, Panic!
            if self.__is_maxhub_panic():
                return None, None

            if os.path.isdir(self.watcher_path) and os.path.exists(self.file_path):
                break

            # Printer().cprint([" ---- sleeping @ ", tick])
            sleep(1)

            tick += 1

        if tick > this_timeout:
            # Printer().cprint(" Lelah menunggu .. data tak kunjung datang ..")
            return False, None
        else:
            # Printer().cprint(" ..... dapat cuy datanya ..")
            data = self.__collect_udp_data()
            self.__deleting_on_read()
            return True, data


