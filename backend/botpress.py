
import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'botpress': 'aIvqrv1yyQTVsk-tp85mRoZx',
}
endpoint = "http://localhost:8000/api/user/botpress/NJ02MW-1YyP8K3fNQrE0s7Jk"

get_response = requests.get(endpoint, headers=headers)
print(get_response.json())
