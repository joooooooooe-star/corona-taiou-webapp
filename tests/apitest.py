import requests

URL = "http://127.0.0.1:5000/api/v1/name"
PARAMS = {'name': 'Joseph'}

r = requests.get(url=URL, params=PARAMS)
print(r)
