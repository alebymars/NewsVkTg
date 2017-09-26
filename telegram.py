import requests


def send_text_message(token, text, chat_id):
    url = 'https://api.telegram.org/bot'

    message_data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }

    try:
        request = requests.post(url+token+'/sendMessage', data=message_data)
    except:
        print('Send message error')
        return False

    return request.content
