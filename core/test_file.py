# #Requests Library
#
#
# # from datetime import datetime
# #
# #
# # date = 'Mar 11th, 2022'
# #
# # print(date)
# # print(type(date))
# #
# # date_format = datetime.strptime(date, '%b %dth, %Y')
# # print(type(date_format))
# #
# # print(date_format.strftime("%b %dth, %Y"))
# import json
#
# import requests
# from requests.exceptions import HTTPError
#
# response = requests.get('https://api.github.com/search/repositories', params=[('q', 'requests+language:python')])
# print(response.raw)
# print(response.url)
# json_response = response.json()
# item = json_response.get('items')[0]
# item_name = item.get('name')
# print(item_name)
#
# print(response)
# print(response.headers)
#
# payload = {'key1': "value1", "key2": "value2"}
# r = requests.post("https://httpbin.org/post", data=payload)
# print(r.url)
#
# payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
# r1 = requests.post('https://httpbin.org/post', data=payload_tuples)
# print(r1.text)
#
# payload_dict = {'key1': ['value1', 'value2']}
# r2 = requests.post('https://httpbin.org/post', data=payload_dict)
# print(r2.text)
#
#
#
#
# # for url in ['https://api.github.com']:
# #     try:
# #         response = requests.get(url)
# #         print(response.content)
# #         print(response.headers.get('content-type'))
# #
# #         # If the response was successful, no Exception will be raised
# #         response.raise_for_status()
# #     except HTTPError as http_err:
# #         print(f'HTTP error occurred: {http_err}')
# #     except Exception as err:
# #         print(f'Other error occurred: {err}')
# #     else:
# #         print('Success!')
#
#
# class Student:
#
#     def __init__(self, name, dept):
#         self.name = name
#         self.dept = dept
#
#     def __str__(self):
#         return f'{self.name} and his department is  {self.dept}'
#
#
# s = Student("Test Student", "ECE")
# print(s)

# Python program to demonstrate
# use of a class method and static method.
from datetime import date


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(self.name)
        print(self.age)

    # a class method to create a
    # Person object by birth year.
    @classmethod
    def from_birth_year(cls, name, year):
        return cls(name, date.today().year - year)

    # a static method to check if a
    # Person is adult or not.
    @staticmethod
    def is_adult(age):
        return age > 18


person1 = Person('Test', 21)
person2 = Person.from_birth_year('Test', 1995)

# print(person1.age)
# print(person2.age)

# print the result
print(Person.is_adult(22))
