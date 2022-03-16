# from datetime import datetime
#
#
# date = 'Mar 11th, 2022'
#
# print(date)
# print(type(date))
#
# date_format = datetime.strptime(date, '%b %dth, %Y')
# print(type(date_format))
#
# print(date_format.strftime("%b %dth, %Y"))
import json

import requests
from requests.exceptions import HTTPError

response = requests.get('https://api.github.com/search/repositories', params=[('q', 'requests+language:python')])
print(response.raw)
print(response.url)
json_response = response.json()
item = json_response.get('items')[0]
item_name = item.get('name')
print(item_name)

print(response)
print(response.headers)

payload = {'key1': "value1", "key2": "value2"}
r = requests.post("https://httpbin.org/post", data=payload)
print(r.url)
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)
print(r1.text)
payload_dict = {'key1': ['value1', 'value2']}
r2 = requests.post('https://httpbin.org/post', data=payload_dict)
print(r2.text)

url = 'https://httpbin.org/post'
files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
m = requests.post(url, files=files)
print(m.text)


# for url in ['https://api.github.com']:
#     try:
#         response = requests.get(url)
#         print(response.content)
#         print(response.headers.get('content-type'))
#
#         # If the response was successful, no Exception will be raised
#         response.raise_for_status()
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#     else:
#         print('Success!')
