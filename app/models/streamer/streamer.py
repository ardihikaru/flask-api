from app import local_settings, rc_streamer, rc_live_stream
from app.addons.utils import (
    get_json_template
)
from app.addons.database_blacklist.blacklist_helpers import (
    extract_identity
)
from app.addons.redis.translator import redis_get, redis_set
from app.models.streamer.streamer_model import StreamerModel
from app.models.streamer.live_streaming_model import LiveStreamingModel

class Streamer():
    stream_source = local_settings["stream_source"]

    def to_dict(self):
        return None

    def insert(self, streamer_data):
        streamer_id = self.stream_source[streamer_data["stream_source"]] + "-" + streamer_data["username"]
        existed_streamer = redis_get(rc_streamer, streamer_id)
        if existed_streamer is not None:
            return False, existed_streamer, "This Streamer is already in database."
        else: # new streamer
            redis_set(rc_streamer, streamer_id, streamer_data)
            return False, streamer_data, "A new Streamer has been recorded into database."

    def update_streaming_data(self, streamer_id, new_data):
        if not new_data["is_streaming"]:
            rc_streamer.delete(streamer_id)
        else:
            live_streaming_obj = LiveStreamingModel()
            live_streaming_obj.set_input_model(streamer_id, new_data)
            is_valid, live_stream_data, msg = live_streaming_obj.get_input_model()
            redis_set(rc_live_stream, streamer_id, live_stream_data)

    def update(self, streamer_id, new_data):
        old_data = redis_get(rc_streamer, streamer_id)
        updated_data = old_data
        for key in old_data:
            if key in new_data:
                if key == "played_games" and len(new_data[key]) > 0:
                    for idx, played_game in enumerate(new_data[key]):
                        new_data[key][idx] = played_game.upper()
                updated_data[key] = new_data[key]
        redis_set(rc_streamer, streamer_id, updated_data)

        if "is_streaming" in new_data:
            self.update_streaming_data(streamer_id, new_data)
            if new_data["is_streaming"]:
                updated_data["stream_url"] = new_data["stream_url"]

        return updated_data

    def delete(self, streamer_id):
        rc_streamer.delete(streamer_id)

    def adding_streamer(self, encoded_token, json_data):
        logged_username = extract_identity(encoded_token)["username"]
        if not self.__is_admin(logged_username):
            return get_json_template(response=False, results=None, total=-1,
                                     message="You do not have access to this feature.")
        streamer_obj = StreamerModel()
        streamer_obj.set_input_model(json_data)
        is_valid, json_data, msg = streamer_obj.get_input_model()

        if not is_valid:
            return get_json_template(response=is_valid, results=json_data,
                                     message=msg, total=-1)

        is_exist, results, msg = self.insert(json_data)

        return get_json_template(is_exist, results, -1, msg)

    def __get_by_streamer_id(self, streamer_id):
        return redis_get(rc_streamer, streamer_id)

    def __get_streamer_by_stsource(self, stsource):
        streamers = []
        for streamer_id in rc_streamer.keys():
            key_source = streamer_id.split('-')[0]
            streamer = self.__get_by_streamer_id(streamer_id)
            if key_source == stsource:
                streamers.append(streamer)
        return streamers

    def get_streamer(self, istreamer_id):
        if istreamer_id == "all":
            streamers = []
            for streamer_id in rc_streamer.keys():
                streamer = self.__get_by_streamer_id(streamer_id)
                streamers.append(streamer)
            return get_json_template(response=True, results=streamers, total=len(streamers), message="Users have been collected.")
        elif istreamer_id in self.stream_source:
            streamer_stsource = self.__get_streamer_by_stsource(self.stream_source[istreamer_id])
            return get_json_template(response=True, results=streamer_stsource, total=len(streamer_stsource), message="Users have been collected.")
        else:
            user = self.__get_by_streamer_id(istreamer_id)
            msg = "Streamer found." if user is not None else "Streamer NOT FOUND."
            return get_json_template(response=True, results=user, total=-1, message=msg)

    def __is_admin(self, username):
        admins = [
            "ardihikaru3@gmail.com",
            "fahim.bagar@gmail.com"
        ]
        if username in admins:
            return True
        else:
            return False

    def updating_streamer(self, encoded_token, streamer_id, new_data):
        logged_username = extract_identity(encoded_token)["username"]
        if self.__is_admin(logged_username):
            updated_data = self.update(streamer_id, new_data)
            return get_json_template(response=True, results=updated_data, total=-1,
                                    message="You information has been updated.")
        else:
            return get_json_template(response=False, results=None, total=-1,
                                     message="You do not have access to this feature.")

    def deleting_streamer(self, encoded_token, target_streamer_id):
        logged_username = extract_identity(encoded_token)["username"]
        existed_streamer = redis_get(rc_streamer, target_streamer_id)
        if existed_streamer is None:
            return get_json_template(response=False, results=None, total=-1,
                                     message="Streamer not Found.")

        if self.__is_admin(logged_username):
            self.delete(target_streamer_id)
            result = {"deleted_streamer_id": target_streamer_id}
            return get_json_template(response=True, results=result, total=-1, message="Streamer [%s] has been deleted." % target_streamer_id)
        else:
            return get_json_template(response=False, results=None, total=-1, message="You do not have access to this feature.")

    def get_played_games(self, streamer_id):
        played_games = redis_get(rc_streamer, streamer_id)["played_games"]
        return get_json_template(response=True, results=played_games, total=len(played_games),
                                 message="Data have been collected.")

    def get_gamer_of(self, game_title):
        game_title = game_title.upper().replace('-', ' ')
        list_of_users = []
        for username in rc_streamer.keys():
            user = redis_get(rc_streamer, username)
            played_games = user["played_games"]
            if game_title in played_games:
                list_of_users.append(user)

        return get_json_template(response=True, results=list_of_users, total=len(list_of_users),
                                 message="Gamer of [%s] has been collected."  % game_title)

    def get_live_streamers(self, stsource=None):
        if stsource.lower() not in self.stream_source:
            return get_json_template(response=False, results=None, total=-1,
                                     message="Unable to recognize Stream Source.")

        active_streamers = []
        for streamer_id in rc_streamer.keys():
            streamer = redis_get(rc_streamer, streamer_id)
            if streamer["is_streaming"]:

                live_stream_data = redis_get(rc_live_stream, streamer_id)
                streamer["stream_url"] = live_stream_data["stream_url"]
                streamer["streaming_time"] = live_stream_data["streaming_time"]

                if stsource is not None:
                    stsource = stsource.lower()
                    if stsource == streamer["stream_source"]:
                        active_streamers.append(streamer)
                else:
                    active_streamers.append(streamer)
        return get_json_template(response=True, results=active_streamers, total=len(active_streamers),
                                 message="Active streamers have been collected.")

