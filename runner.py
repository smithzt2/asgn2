import requests
from requests.auth import HTTPDigestAuth

url = 'https://smithping.herokuapp.com/ping'
r = requests.get(url, auth=HTTPDigestAuth('vcu', 'rams'))
print(r.text)
