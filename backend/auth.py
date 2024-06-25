import requests

data = {
    'username': 'fahdsoliman',
    'password': 'milanforever'
}
url = 'http://localhost:8000/api/auth/'
response = requests.post(url=url, data=data)
print(response.json())