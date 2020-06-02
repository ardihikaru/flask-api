import os, shutil
import simplejson as json

def is_localhost():
    root_dir        = os.path.dirname(os.path.abspath(__file__)).replace("app", "")
    file_path = root_dir + "url_host.json"
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')

    url = json.loads(data)["host"]
    domain = url.split("//")[-1].split("/")[0]
    if "localhost" in domain:
        return True
    else:
        return False

def init_folders(local_settings):
    idngamer_path = "app/data"
    idngamer_res_path = "app/data/resources"
    log_path = local_settings["log_path"]
    log_login_path = local_settings["logging_login_path"]
    if not os.path.isdir(idngamer_path):
        os.makedirs(idngamer_path)
    if not os.path.isdir(idngamer_res_path):
        os.makedirs(idngamer_res_path)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    if not os.path.isdir(log_login_path):
        os.makedirs(log_login_path)