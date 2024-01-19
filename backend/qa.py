from datetime import date, datetime
import requests

headers = {
    "Authorization":  "nans 4dfe28da961227ab65c338024079249fccac7396"
}

data = {
    'q': 'كم يتطلب عمل حتى يتم حجز النطاق السوري؟',
}
endpoint = "http://localhost:8000/qa/predict/answer/"

get_response = requests.post(endpoint, headers=headers, data=data)
print(get_response.json())