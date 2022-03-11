from datetime import datetime


date = 'Mar 11th, 2022'

print(date)
print(type(date))

date_format = datetime.strptime(date, '%b %dth, %Y')
print(type(date_format))

print(date_format.strftime("%b %dth, %Y"))

