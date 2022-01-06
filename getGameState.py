from toBase64 import port
from api import call

BASE_URL = f"https://127.0.0.1:{port}"

# None, Lobby, Matchmaking, ChampSelect, InProgress, endgame?

def getGameState():
    url = BASE_URL + "/lol-gameflow/v1/gameflow-phase"
    return call(url)
