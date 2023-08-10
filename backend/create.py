from datetime import date, datetime
import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'user': 55,
    'my_product': 12,
    'domain_name': 'http://www.apitest2.sy',
    'note': f'<p dir="rtl">created with botpress, Date: {datetime.now()}</p>'
}
endpoint = "http://localhost:8000/api/product/1/resdomain/"

get_response = requests.post(endpoint, headers=headers, data=data)
print(get_response.json())