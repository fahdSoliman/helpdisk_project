import requests
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
from django.utils.safestring import SafeString
import urllib3


url = 'https://aws.amazon.com/ar/what-is/web-hosting/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

http = urllib3.PoolManager()
article_tags = ['p', 'b', 'div', 'a']
article_texts = []

try:
    response = http.request('GET', url=url)

    if response.status == 200:
        html = response.data
        soup = BeautifulSoup(html, 'html.parser')
        for tag in article_tags:
            elements = soup.find_all(tag)
            for element in elements:
                next_element = element
                while next_element:
                    article_texts.append(''.join(next_element.findAll(text=True)))
                    next_element = next_element.find_next_sibling(tag)

        article_text = '\n'.join(article_texts)
        print(article_text)
except Exception as e:
    print(f"Error fetching URL: {e}")






# res = requests.get(url, headers=header)

# cont = res.content

# print(cont)
# soup = BeautifulSoup(cont, 'html.parser')


# name = soup.find_all('title')[0]
# name_clean = strip_tags(name)
# print(name)
# print(str.replace(name_clean, '\n', ' '))
# print(res.headers)