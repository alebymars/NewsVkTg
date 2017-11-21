import os
import time
import json

import vk
import telegram


def get_config():
    file_path = os.path.join('.', "config.json")
    with open(file_path, 'r', encoding="UTF8") as f:
        config = json.load(f)
    return config


CONFIG = get_config()
TIMESTAMP = int(time.time())


def callback_two_factor_auth():
    offset = telegram.get_last_update_id(CONFIG["telegram"]["key"])
    telegram.send_text_message(CONFIG["telegram"]["key"], "Enter authentication code: ", CONFIG["telegram"]["admin_id"])
    key = telegram.get_text_message(CONFIG["telegram"]["key"], CONFIG["telegram"]["admin_id"], offset)
    remember_device = True
    return key, remember_device


def send_messages(data, config):
    for post in data[::-1]:
        text_message = ''
        if "attachments" in post:
            for att in post["attachments"]:
                if "photo" in att:
                    text_message += '<a href="{}">🍀 \n</a>'.format(att["photo"]["photo_130"])
                    break
                if "audio" in att:
                    text_message += '<i>Музыка по ссылке в вк =) </i>\n'
                    break
                if "video" in att:
                    text_message += '<a href="{}">Видео по ссылке в вк =) </a>\n'.format(att["video"]["photo_130"])
                    break
        text_message += "<b>{}</b>".format(vk.get_user(CONFIG["vk"], callback_two_factor_auth, post["from_id"]))
        if post["text"] != '':
            text_message += "\n\n{}\n ".format(post["text"])
        text_message += "\n<a href='https://vk.com/feed?w=wall{}_{}'>ссылка на вк</a> \n ".format(post["owner_id"],
                                                                                                  post["id"])
        telegram.send_text_message(config["key"], text_message, config["chat_id"])


def main():
    data_vk = vk.get_news(CONFIG["vk"], callback_two_factor_auth)
    send_messages(data_vk, CONFIG["telegram"])

    file_path = os.path.join('.', "timestamp")
    file_timestamp = open(file_path, 'w')
    file_timestamp.write(str(TIMESTAMP))
    file_timestamp.close()


if __name__ == "__main__":
    main()
