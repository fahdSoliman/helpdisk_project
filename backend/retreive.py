from datetime import date, datetime
import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

endpoint = "http://localhost:8000/api/product/vps/3/"

get_response = requests.get(endpoint, headers=headers)
print(get_response.json())

body = get_response.json()
note = body['note']
new_note = note + ''
data = {
    'note': note + '<p>تم الارسال عن طريق بايثون</p>'
}
post_resopnse = requests.patch(endpoint,headers=headers, data=data)
# print(data2['note'])
print(post_resopnse.json())
