import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'user': 99,
    'my_product': 5,
    'domain_name': 'http://www.geographic.sy',
}
endpoint = "http://localhost:8000/api/product/2/resdomain/"

get_response = requests.put(endpoint, headers=headers, data=data)
print(get_response.json())