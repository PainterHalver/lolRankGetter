from toBase64 import port
from api import call, BASE_URL

# None, Lobby, Matchmaking, ChampSelect, InProgress, endgame?

class GameState:
    NONE: "None"
    LOBBY: "Lobby"
    MATCHMAKING: "Matchmaking"
    CHAMPSELECT: "ChampSelect"
    INPROGRESS: "InProgress"

def getGameState():
    url = BASE_URL + "/lol-gameflow/v1/gameflow-phase"
    return call(url)
