import requests

id = input(f'inter the id:\n ')
# print('enter the id: \n')

endpoint = f"http://localhost:8000/api/product/{id}"


get_response = requests.get(endpoint)
print(get_response.json())


