import os
import time
import json

import vk
import telegram

import log


def get_config():
    file_path = os.path.join('.', "config.json")
    with open(file_path, 'r', encoding="UTF8") as f:
        config = json.load(f)
    return config


CONFIG = get_config()
TIMESTAMP = int(time.time())

# Инициализация логов
lg = log.create_log(debug=CONFIG["logger"]["debug"], filename=__file__[:-3])


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
                    if 'photo_'+str(att['photo']['width']) in att["photo"]:
                        text_message += f'<a href="{att["photo"]["photo_"+str(att["photo"]["width"])]}">🍀 \n</a>'
                    else:
                        text_message += f'<a href="{att["photo"]["photo_130"]}">🍀 \n</a>'
                    break
                if "audio" in att:
                    text_message += '<i>Музыка по ссылке в вк =) </i>\n'
                    break
                if "video" in att:
                    text_message += f'<a href="{att["video"]["photo_130"]}">Видео по ссылке в вк =) </a>\n'
                    break
        text_message += f"<b>{vk.get_user(CONFIG['vk'], callback_two_factor_auth, post['from_id'])}</b>"
        if post["text"] != '':
            text_message += f"\n\n{post['text']}\n "
        text_message += f"\n<a href='https://vk.com/feed?w=wall{post['owner_id']}_{post['id']}'>ссылка на вк</a> \n "
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
