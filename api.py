import toBase64
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def call(url):
    response = requests.get(url, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    return json.loads(response.text)
