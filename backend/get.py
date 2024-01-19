import requests
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
from django.utils.safestring import SafeString

url = 'https://arfiles.net/241/6/SVU/TSP%20Codec.rar'

res = requests.get(url)

cont = res.content


# soup = BeautifulSoup(cont, 'html.parser')


# name = soup.find_all('title')[0]
# name_clean = strip_tags(name)
# print(name)
# print(str.replace(name_clean, '\n', ' '))
print(res.headers)