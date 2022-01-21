from api import call, BASE_URL
from Summoner import Summoner
from GameState import GameState
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(10)


def getPlayer(player):
    return Summoner(summonerId=player["summonerId"])


def getAllChampSelect():
    data = call(f"{BASE_URL}/lol-champ-select/v1/session")
    myTeam = data["myTeam"]

    allies = pool.map(getPlayer, myTeam)

    return allies


def getAllInProgress():
    data = call(f"{BASE_URL}/lol-gameflow/v1/session")
    gameData = data["gameData"]
    teamOne = gameData["teamOne"]
    teamTwo = gameData["teamTwo"]

    allSums = []
    allSums = allSums + pool.map(getPlayer, teamOne)
    allSums = allSums + pool.map(getPlayer, teamTwo)
    return allSums


def getRank(gameState):
    all = []
    if gameState == GameState.CHAMPSELECT:
        all = getAllChampSelect()
    elif gameState == GameState.INPROGRESS:
        all = getAllInProgress()

    # https://stackoverflow.com/questions/40939078/pandas-dataframe-in-multiple-threads
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
