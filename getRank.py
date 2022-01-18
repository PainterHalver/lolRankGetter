from api import call, BASE_URL
from Summoner import Summoner
from GameState import GameState
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool


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
    all = []
    if gameState == GameState.CHAMPSELECT:
        all = getAllChampSelect()
    elif gameState == GameState.INPROGRESS:
        all = getAllInProgress()

    # soloDataframe = pd.DataFrame(columns=['Name', 'Rank', 'LP', 'Wins', "Last 20 Games"])
    # flexDataframe = pd.DataFrame(columns=['Name', 'Rank', 'LP', 'Wins', "Last 20 Games"])

    # https://stackoverflow.com/questions/40939078/pandas-dataframe-in-multiple-threads
    pool = ThreadPool(10)

    def getSoloData(player):
        return {
            "Name": player.name,
            "Rank": f"{player.rankedStats.RANKED_SOLO_5x5['tier']} {player.rankedStats.RANKED_SOLO_5x5['division']}",
            "LP": f"{player.rankedStats.RANKED_SOLO_5x5['leaguePoints']} LP",
            "Wins": player.rankedStats.RANKED_SOLO_5x5['wins'],
            "Last 20 Games": f"{player.matchHistory.last20} ({player.matchHistory.winCount}W / {player.matchHistory.loseCount}L)"
        }
    def getFlexData(player):
        return {
            "Name": player.name,
            "Rank": f"{player.rankedStats.RANKED_FLEX_SR['tier']} {player.rankedStats.RANKED_FLEX_SR['division']}",
            "LP": f"{player.rankedStats.RANKED_FLEX_SR['leaguePoints']} LP",
            "Wins": player.rankedStats.RANKED_FLEX_SR['wins'],
            "Last 20 Games": f"{player.matchHistory.last20} ({player.matchHistory.winCount}W / {player.matchHistory.loseCount}L)"
        }
    resultsSolo = pool.map(getSoloData, all)
    resultsFlex = pool.map(getFlexData, all)

    soloDataframe = pd.DataFrame(resultsSolo)
    flexDataframe = pd.DataFrame(resultsFlex)

    print(soloDataframe)
    print("-------------------------------------------------------------------------")
    print(flexDataframe)
