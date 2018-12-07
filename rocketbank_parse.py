import json
import tqdm
import requests
from requests import Session
session = Session()
session.verify = "charles-ssl-proxying-certificate.pem"

token = '<token goes here>'
params = {'token': token, 'page': 1, 'per_page': 999999}
x_device_id = 'F28DE743-6F13-4273-A25C-37D9716752CA'
x_time = '1544142041'
x_sig = '00aae46e8cb83b48b9238f75bf3fc62e'
headers = {'x-device-id': x_device_id, 'x-time': x_time, 'x-sig': x_sig}

response = requests.get('https://rocketbank.ru/api/v5/operations/sexy_feed', params=params, headers=headers, verify=False)

operations = []
feed = response.json()['feed']

for item in tqdm.tqdm(feed):
    if item[0] == 'operation':
        operation = item[1]
        merchant_name = operation['merchant']['name']
        receipt_url = operation['receipt_url']
        cost = operation['money']['amount']
        receipt = requests.get(receipt_url, verify=False)
        operations.append(receipt.text)

json.dump(operations, open("rocketbank.json", "w"))
