import requests


endpoint = f"http://localhost:8000/api/product/"


get_response = requests.get(endpoint)
print(get_response.json())
