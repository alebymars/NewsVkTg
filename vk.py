import os

import vk_api


def _vk_auth(config, callback_two_factor_auth):
    vk_session = vk_api.VkApi(
        config["login"], config["password"],
        auth_handler=callback_two_factor_auth
    )

    vk_session.auth()

    return vk_session.get_api()


def get_user(config, callback_two_factor_auth, id_user):
    if id_user > 0:
        vk = _vk_auth(config, callback_two_factor_auth)
        res = vk.users.get(user_ids=id_user)
        return f"{res[0]['first_name']} {res[0]['last_name']}"
    else:
        for gr in config["id_list"]:
            if gr["id"] == id_user:
                return gr["name"]
        else:
            return "ОШИБКА"


def get_news(config, callback_two_factor_auth):
    vk = _vk_auth(config, callback_two_factor_auth)

    file_path = os.path.join('.', "timestamp")
    timestamp = open(file_path).read()

    def _get_news_from_wall(local_owner_id):
        data_local = []
        offset = 0
        while offset >= 0:
            items = vk.wall.get(owner_id=local_owner_id, offset=offset)
            for item in items["items"]:
                if int(item["date"]) > int(timestamp):
                    data_local.append(item)
                else:
                    offset = -1
                    break
                offset += 25

        return data_local

    data = []
    for owner_id in config['id_list']:
        data.extend(_get_news_from_wall(owner_id["id"]))

    return data
