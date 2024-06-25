from datetime import date, datetime
import requests

headers = {
    "Authorization":  "nans 852ba4771f0a21f81bd74132870847fcf26fa79f"
}

endpoint = "http://localhost:8000/qa/api/araELECTRA/predict/"


data = {
    'question': 'كم يتطلب وقت حجز النطاق لتفعيله على مخدم الاسماء'
}
post_resopnse = requests.post(endpoint,headers=headers, json=data)
# print(data2['note'])
print(post_resopnse.json())
