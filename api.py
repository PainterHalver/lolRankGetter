import toBase64
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from toBase64 import port

BASE_URL = f"https://127.0.0.1:{port}"

def call(url):
    response = requests.get(url, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    return json.loads(response.text)
