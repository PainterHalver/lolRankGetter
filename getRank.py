from api import call, BASE_URL
from Summoner import Summoner
from GameState import GameState
import pandas as pd


def getAllChampSelect():
    data = call(f"{BASE_URL}/lol-champ-select/v1/session")
    myTeam = data["myTeam"]
    allies = []
    for player in myTeam:
        allies.append(Summoner(summonerId=player["summonerId"]))
    return allies


def getAllInProgress():
    data = call(f"{BASE_URL}/lol-gameflow/v1/session")
    gameData = data["gameData"]
    allSums = []
    for p in gameData["teamOne"]:
        if "summonerId" in p:
            allSums.append(Summoner(summonerId=int(p["summonerId"])))
    for p in gameData["teamTwo"]:
        if "summonerId" in p:
            allSums.append(Summoner(summonerId=int(p["summonerId"])))
    return allSums


def getRank(gameState):
    if gameState == GameState.CHAMPSELECT:
        all = getAllChampSelect()
    elif gameState == GameState.INPROGRESS:
        all = getAllInProgress()
    soloDataframe = pd.DataFrame(columns=['Name', 'Rank', 'LP', 'Wins', "Last 20 Games"])
    for p in all:
        soloDataframe = soloDataframe.append({
            "Name": p.name,
            "Rank": f"{p.rankedStats.RANKED_SOLO_5x5['tier']} {p.rankedStats.RANKED_SOLO_5x5['division']}",
            "LP": f"{p.rankedStats.RANKED_SOLO_5x5['leaguePoints']} LP",
            "Wins": p.rankedStats.RANKED_SOLO_5x5['wins'],
            "Last 20 Games": f"{p.matchHistory.last20} ({p.matchHistory.winCount}W / {p.matchHistory.loseCount}L)"
        }, ignore_index=True)
    flexDataframe = pd.DataFrame(columns=['Name', 'Rank', 'LP', 'Wins', "Last 20 Games"])
    for p in all:
        flexDataframe = flexDataframe.append({
            "Name": p.name,
            "Rank": f"{p.rankedStats.RANKED_FLEX_SR['tier']} {p.rankedStats.RANKED_FLEX_SR['division']}",
            "LP": f"{p.rankedStats.RANKED_FLEX_SR['leaguePoints']} LP",
            "Wins": p.rankedStats.RANKED_FLEX_SR['wins'],
            "Last 20 Games": f"{p.matchHistory.last20} ({p.matchHistory.winCount}W / {p.matchHistory.loseCount}L)"
        }, ignore_index=True)
    print(soloDataframe)
    print("-------------------------------------------------------------------------")
    print(flexDataframe)
