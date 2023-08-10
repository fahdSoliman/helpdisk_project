import requests


headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

endpoint = f"http://localhost:8000/api/user/53/profile/"

data = {
    "gender": "1",
}

get_response = requests.put(endpoint, headers=headers, json=data)
print(get_response.json())

