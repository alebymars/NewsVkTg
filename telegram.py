import requests

URL = 'https://api.telegram.org/bot'


def send_text_message(token, text, chat_id):
    message_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    print(text)
    request = requests.post(URL+token+'/sendMessage', data=message_data)
    print(request.content)
    return request.content


def get_last_update_id(token):
    message_data = {
        'offset': 0,
        'timeout': 1
    }
    response = requests.post(URL + token + '/getUpdates', data=message_data)
    data = response.json()
    if 'result' in data:
        if data['result']:
            return data['result'][-1]['update_id']
        else:
            return 0


def get_text_message(token, chat_id, offset):
    while True:
        message_data = {
            'offset': offset + 1,
            'timeout': 100
        }
        response = requests.post(URL + token + '/getUpdates', data=message_data)
        data = response.json()
        if 'result' in data:
            data['result'].reverse()
            for result in data['result']:
                if result["message"]["from"]["id"] == chat_id:
                    return result['message']['text']
    return 0

