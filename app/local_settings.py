
class LocalSettings:
    __shared_state = {
            "queue_config": {
                "main_path": "app/data/resources/queue/",
                "pool_size": 2,
                "prefix": "queue-"
            },
            "logging_login_path": "app/data/resources/logs/login/",
            "log_path"              : "app/data/resources/logs",
            "stream_source": {
                "facebook": "fb",
                "youtube": "yt",
                "twitch": "twt"
            },
            # "inotify_config"       : {
            #     "default_dir"   : "app/data/resources/tick/",
            #     "default_name"  : "data.json"
            # },
            # "udp_config"       : {
            #     "port"  : 3000,
            #     "stored_response"   : "app/data/clients/",
            #     "timeout"   : 3,
            #     "extra_timeout"   : 12,
            #     "cmd"   : {
            #         "start_bot"     : "start",
            #         "check_strategy": "check"
            #     },
            #     "output"   : {
            #         "start_bot"     : "buy",
            #         "echo": "echo",
            #         "error": "error"
            #     }
            # }
            "android_key"               : "80If2wqGin-aJ-Kg0U89zj8cazTGKXdm7UULtgdnExI="
        }
    def __init__(self):
        self.__dict__ = self.__shared_state

    def extract(self):
        return self.__shared_state

local_settings  = LocalSettings().extract()
