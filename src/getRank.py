import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils import toBase64

SOLODUO = "rank5solo"
FLEX = "rank5flex"
CURRENTSEASON = "11"

def gameCount(queueType, puuid, season):
    url = f"https://127.0.0.1:{toBase64.port}/lol-career-stats/v1/summoner-games/{puuid}/season/{season}"
    x = requests.get(url, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    count = 0
    for i in y:
        if i["queueType"] == queueType:
            count += 1
    return count

# NAME TO PUUID CODE
def nameToPuuid(name):
    nameToPuuidUrl = f"https://127.0.0.1:{toBase64.port}/lol-summoner/v1/summoners?name={name}"
    x = requests.get(nameToPuuidUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    puuid = y["puuid"]
    return puuid

# SUMID TO PUUID CODE
def sumIDToPuuid(sumID):
    sumIDToPuuidUrl = f"https://127.0.0.1:{toBase64.port}/lol-summoner/v1/summoners/{sumID}"
    x = requests.get(sumIDToPuuidUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    puuid = y["puuid"]
    return puuid

# SUMID TO NAME
def sumIDToName(sumID):
    sumIDToNameUrl = f"https://127.0.0.1:{toBase64.port}/lol-summoner/v1/summoners/{sumID}"
    x = requests.get(sumIDToNameUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    name = y["displayName"]
    return name

# NAME TO SUMID
def nameToSumID(name):
    nameToSumIDUrl = f"https://127.0.0.1:{toBase64.port}/lol-summoner/v1/summoners?name={name}"
    x = requests.get(nameToSumIDUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    sumID = y["summonerId"]
    return sumID

# PUUID TO RANKED INFO
def puuidToRankedSolo(puuid):
    puuidToRankedSoloUrl = f"https://127.0.0.1:{toBase64.port}/lol-ranked/v1/ranked-stats/{puuid}"
    x = requests.get(puuidToRankedSoloUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    soloStats = (y["queueMap"]["RANKED_SOLO_5x5"])
    return soloStats

# GET SUMID IN LOBBY
allySumIDs = []
def getAllAllySumID():
    getAllSumIDUrl = f"https://127.0.0.1:{toBase64.port}/lol-champ-select/v1/session"
    x = requests.get(getAllSumIDUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    myTeam = y["myTeam"]
    global allySumIDs
    allySumIDs = []
    for i in range(len(myTeam)):
        allySumIDs.append(myTeam[i]["summonerId"])
    return allySumIDs

# LOBBY TO INFO
def lobbyInit():
    for sumID in getAllAllySumID():
        name = sumIDToName(sumID)
        puuid = sumIDToPuuid(sumID)
        soloStats = puuidToRankedSolo(puuid)
        tier = soloStats["tier"]
        division = soloStats["division"]
        lp = soloStats["leaguePoints"]
        winCount = int(soloStats["wins"])
        lostCount = int(soloStats["losses"])
        point = "point"
        points = "points"
        if tier == "NONE":
            print(f"{name}: Unranked")
        else:
            print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}, {winCount} wins {gameCount(SOLODUO, puuid, CURRENTSEASON)-winCount} losses, {round(winCount/(gameCount(SOLODUO, puuid, CURRENTSEASON))*100,2)}% winrate")


# GET ENEMY "summonerInternalName" when game starts loading
def filterAllySumIDs(variable):
    global allySumIDs
    if (variable in allySumIDs):
        return False
    else:
        return True

def getEnemySumIDs():
    getEnemyNameUrl = f"https://127.0.0.1:{toBase64.port}/lol-gameflow/v1/session"
    x = requests.get(getEnemyNameUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    gameData = y["gameData"]
    allSumIDs = []
    for i in gameData["teamOne"]:
        if "summonerId" in i:
            allSumIDs.append(int(i["summonerId"]))
    for i in gameData["teamTwo"]:
        if "summonerId" in i:
            allSumIDs.append(int(i["summonerId"]))
    enemySumIDs = filter(filterAllySumIDs, allSumIDs)
    return enemySumIDs

def gameStartInit():
    enemySumIDs = getEnemySumIDs()
    if enemySumIDs == []:
        raise Exception("No enemy found!")
    for sumID in enemySumIDs:
        name = sumIDToName(sumID)
        puuid = sumIDToPuuid(sumID)
        soloStats = puuidToRankedSolo(puuid)
        tier = soloStats["tier"]
        division = soloStats["division"]
        lp = soloStats["leaguePoints"]
        winCount = int(soloStats["wins"])
        lostCount = int(soloStats["losses"])
        point = "point"
        points = "points"
        if tier == "NONE":
            print(f"{name}: Unranked")
        else:
            print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}, {winCount} wins {gameCount(SOLODUO, puuid, CURRENTSEASON)-winCount} losses, {round(winCount/(gameCount(SOLODUO, puuid, CURRENTSEASON))*100,2)}% winrate")
