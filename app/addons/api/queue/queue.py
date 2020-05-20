from app import local_settings
from os import path, listdir

class Queue():
    def set_queue_config(self):
        self.main_path      = local_settings["queue_config"]["main_path"]
        self.pool_size      = local_settings["queue_config"]["pool_size"]
        self.prefix         = local_settings["queue_config"]["prefix"]
        self.total_of_tasks = 0
        self.queue_dirs     = self.get_queue_dir()

    def __get_folder_names(self, dir):
        queue_dirs = []
        try:
            queue_dirs = [name for name in listdir(dir) if path.isdir(dir)]
        except:
            pass
        finally:
            return queue_dirs

    def get_queue_dir(self):
        return self.__get_folder_names(self.main_path)

    def get_pool_name(self):
        self.get_queue_dir()
        pool_name = self.prefix + "00"
        pool_path = self.main_path + pool_name
        this_pool_size = len(self.__get_folder_names(pool_path))
        for qp_name in self.queue_dirs:
            q_path = self.main_path + qp_name
            number_of_tasks = len(self.__get_folder_names(q_path))
            if number_of_tasks < this_pool_size:
                pool_name = qp_name
                this_pool_size = number_of_tasks

        return pool_name
