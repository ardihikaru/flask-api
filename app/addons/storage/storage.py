# from app.addons.cryptography.fernet import encrypt, decrypt
from app.addons.utils import is_file_exist, write_to_file, load_file, get_today, delete_file
from app import local_settings
# from app.addons.database.user_login_db import UserMicroDB
# import os

class MyStorage():
    def __init__(self):
        self.log_login_dir   = local_settings["logging_login_path"]

    def __login_data(self, status):
        return {
            "last_login": get_today(),
            "is_login": status
        }

    def logging_login(self, username):
        file_path = self.log_login_dir + username + ".json"
        write_to_file(file_path, self.__login_data(True))

    def logging_logout(self, username):
        file_path = self.log_login_dir + username + ".json"
        write_to_file(file_path, self.__login_data(False))
        # file_path = self.log_login_dir + username + ".json"
        # delete_file(file_path)

    # def saving_token(self, binary_id, token):
    #     dumping_path = self.root_dir + binary_id + ".json"
    #     if not is_file_exist(dumping_path):
    #         # bot_db = MicroDB(rule_id="db", table_type="user", is_main_db=True)
    #         bot_db = UserMicroDB()
    #         try:
    #             record = bot_db.find_by_binaryid(binary_id)[0]
    #             record["token"] = encrypt(token)
    #             bot_db.update_by_id(record, record["__id__"])
    #         except:
    #             pass
    #
    #         write_to_file(dumping_path, encrypt(token))
    #     return True

    # def saving_virtual_token(self, binary_id, token):
    #     dumping_path = self.virtoken_dir + binary_id + ".json"
    #     if not is_file_exist(dumping_path):
    #         bot_db = UserMicroDB()
    #         try:
    #             record = bot_db.find_by_binaryid(binary_id)[0]
    #             record["token"] = encrypt(token)
    #             bot_db.update_by_id(record, record["__id__"])
    #         except:
    #             pass
    #
    #         write_to_file(dumping_path, encrypt(token))
    #     return True

    # def get_token(self, binary_id):
    #     dumping_path = self.root_dir + binary_id + ".json"
    #     if is_file_exist(dumping_path):
    #         data = load_file(dumping_path)
    #         decrypted_data = decrypt(data)
    #         return decrypted_data
    #     return None
    #
    # def get_encrypted_token(self, binary_id):
    #     dumping_path = self.root_dir + binary_id + ".json"
    #     if is_file_exist(dumping_path):
    #         encrypted_data = load_file(dumping_path)
    #         encrypted_data = encrypted_data
    #         return encrypted_data
    #     return None
    #
    # def decrypt_token(self, encrypted_data):
    #     decrypted_data = decrypt(encrypted_data)
    #     return decrypted_data

    # def get_encrypted_virtual_token(self, binary_id):
    #     dumping_path = self.virtoken_dir + binary_id + ".json"
    #     if is_file_exist(dumping_path):
    #         encrypted_data = load_file(dumping_path)
    #         encrypted_data = encrypted_data
    #         return encrypted_data
    #     return None
    #
    # def store_statement(self, binary_id, data):
    #     file_path = self.statement_dir + binary_id + ".json"
    #     write_to_file(file_path, data)

    # def get_statement(self, binary_id):
    #     dumping_path = self.statement_dir + binary_id + ".json"
    #     if is_file_exist(dumping_path):
    #         statement_data = load_file(dumping_path)
    #         return statement_data
    #     return None

