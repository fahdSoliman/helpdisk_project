from datetime import date, datetime
import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'id': 3
}
endpoint = "http://localhost:8000/api/product/resdomain/2/"

get_response = requests.get(endpoint, headers=headers)
print(get_response.json())