from string import digits
from random import choice
import requests
from django.contrib.auth.hashers import make_password

from iwbuy.prod_settings import SMS_RU_API_KEY, CONNECT_URL


# def gen_password():
#     """Генерация и хеширование кода авторизации"""
#     code = list()
#     for i in range(4):
#         code.append(choice(digits))
#     hashed_pin = make_password(''.join(code))
#     pin = ''.join(code)
#     print(pin)
#     return hashed_pin


# TODO: test заменить на 0 при выкладывании на сервер
def send_sms_ru(phone, pin):
    """Отправка sms с кодом авторизации"""
    query = {
        'api_id': SMS_RU_API_KEY,
        'to': phone,
        'msg': pin,
        'json': 1,
        'test': 1
    }
    result = requests.get(CONNECT_URL, params=query).json()
    if result['status'] == 'OK':
        return result
    else:
        return "Ошибка"


