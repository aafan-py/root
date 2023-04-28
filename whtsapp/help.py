import requests

def check_whtsapp_number():
    URL = "https://api.whatsapp.com/send?"

    PARAMS = {
        'phone': 919930432351
    }
    response = requests.get(url=URL, params=PARAMS)
    return response


msg=check_whtsapp_number()

print(msg)