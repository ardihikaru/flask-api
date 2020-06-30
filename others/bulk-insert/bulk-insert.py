import simplejson as json
import argparse
import os
import requests


class BulkInsert:
    def __init__(self, opt):
        self.opt = opt
        self.file_path = opt.input_path + opt.filename

    def run(self):
        if os.path.exists(self.file_path):
            with open(self.file_path) as json_file:
                json_data = json.load(json_file)
                for user_data in json_data:
                    _, _ = self._post_new_user(user_data)  # currently I does not need any use of the response result
        else:
            print(" --- Input json file DOES NOT EXIST!")

    def _post_new_user(self, json_data):
        response = requests.post(self.opt.api_url, json=json_data)
        return response.status_code, response.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--input_path', type=str, default="app/others/bulk-insert/", help="Location of the json file")
    parser.add_argument('--input_path', type=str, default="", help="Location of the json file")
    parser.add_argument('--filename', type=str, default="dummy-user-data.json", help="json filename")
    parser.add_argument('--api_url', type=str, default="http://localhost:5000/api/users", help="target API URL")
    opt = parser.parse_args()
    print(opt)

    BulkInsert(opt).run()
