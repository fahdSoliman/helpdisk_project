import requests

headers = {
    "Authorization":  "nans 852ba4771f0a21f81bd74132870847fcf26fa79f"
}

endpoint = "http://localhost:8000/qa/api/BART_LFQA/predict/"


data = {
    'question': 'لدي استضافة مشتركة قمت بحجزها منذ سنة ولكن وصلني بريد بأن هذه الاستضافة قد تم ايقافها بسبب عدم دفع اجور التمديد، اريد معرفة هل سيتم ايقاف الاستضافة في حال عدم دفع اجور التمديد؟'
}
post_resopnse = requests.post(endpoint,headers=headers, data=data)
# print(data2['note'])
print(post_resopnse.json())
