import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    "fbName": "damascus",
}
endpoint = "http://localhost:8000/api/user/fahdsoliman/"

get_response = requests.post(endpoint, headers = headers, data = data)
print(get_response.json())
