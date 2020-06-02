import time
import simplejson as json
from app import fernet
from app.addons.utils import get_json_template
from app import local_settings

class ServerSideEvent():
    def __init__(self):
        pass

    def get_sse_access(self, user_id, binary_id):
        data = {
            "user_id": user_id,
            "binary_id": binary_id
        }
        dump_data = json.dumps(data)
        message = dump_data.encode()
        encrypted = fernet.encrypt(message).decode('utf8')
        return encrypted

    def get_message(self, resp):
        time.sleep(1.0)
        return resp

    def __get_balance(self, json_data):
        # do: collecting up-to-date Binary BALANCE here
        balance_path = local_settings["balance_dump_path"] + self.binary_id + ".json"
        with open(balance_path, "r") as read_file:
            data = json.load(read_file)
        return data
        # return {"balance": 10000}

    def __extract_data(self, encrypted_data):
        try:
            json_data = json.loads(fernet.decrypt(encrypted_data.encode()).decode('utf8'))
            self.binary_id = json_data["binary_id"]
            balance = self.__get_balance(json_data)
            result = get_json_template(response=True, results=balance, message="Balance collected", total=-1)
        except:
            result = get_json_template(message="Unable to collect balance info", total=-1)

        return result

    def one_time_stream(self, encrypted_data):
        resp = self.__extract_data(encrypted_data)
        # print(resp)
        return resp

    def event_stream(self, encrypted_data):
        ctr = 0
        while True:
            resp = self.__extract_data(encrypted_data)
            ctr += 1
            yield 'data: {}\n\n'.format(self.get_message(resp))