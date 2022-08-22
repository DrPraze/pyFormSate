import requests

BASE = "http://127.0.0.1:5000/getfields"
response = requests.get(BASE+"https://mirrorstoreng.com/register")
print(response.json())
