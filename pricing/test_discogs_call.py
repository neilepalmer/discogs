import requests

url = 'https://api.discogs.com//marketplace/price_suggestions/249504'
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'user-agent': "FooBarApp/3.0",
           'Authorization': 'Discogs token=XdVfgkiKHPbdWPKKYRrGjGxFdFRCWNVSBJHQZIZw'}
r = requests.get(url, headers=headers)
print(r.json())

