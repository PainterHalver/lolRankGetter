import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils import toBase64

def getGameState():
    url = f"https://127.0.0.1:{toBase64.port}/lol-gameflow/v1/gameflow-phase"
    x = requests.get(url, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    return y
