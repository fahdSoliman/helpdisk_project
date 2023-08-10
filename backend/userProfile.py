import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'telegram': 'fahdsoliman',
}
endpoint = "http://localhost:8000/api/user/telegram/fahdsoliman"

get_response = requests.get(endpoint, headers=headers)
print(get_response.status_code)