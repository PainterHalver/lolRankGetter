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
    stats = y["queueMap"]["RANKED_SOLO_5x5"]
    return stats

def puuidToRankedFlex(puuid):
    puuidToRankedFlexUrl = f"https://127.0.0.1:{toBase64.port}/lol-ranked/v1/ranked-stats/{puuid}"
    x = requests.get(puuidToRankedFlexUrl, headers={"Authorization": f"Basic {toBase64.authCode}"}, verify=False)
    y = json.loads(x.text)
    stats = y["queueMap"]["RANKED_FLEX_SR"]
    return stats

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
def render(stats, name, puuid, queueType):
    tier = stats["tier"]
    division = stats["division"]
    lp = stats["leaguePoints"]
    winCount = int(stats["wins"])
    lostCount = int(stats["losses"])
    point = "point"
    points = "points"
    if tier == "NONE":
        print(f"{name}: Unranked")
    else:
        print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}, {winCount} wins {gameCount(queueType, puuid, CURRENTSEASON)-winCount} losses, {round(winCount/(gameCount(queueType, puuid, CURRENTSEASON))*100,2)}% winrate")    

def lobbyInit():
    for sumID in getAllAllySumID():
        name = sumIDToName(sumID)
        puuid = sumIDToPuuid(sumID)
        stats = puuidToRankedSolo(puuid)
        render(stats, name, puuid, SOLODUO)
        


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
    enemySumIDs = []
    enemySumIDs = filter(filterAllySumIDs, allSumIDs)
    return enemySumIDs

def gameStartInit(queueType):
    enemySumIDs = getEnemySumIDs()
    if enemySumIDs == []:
        raise Exception("No enemy found!")
    for sumID in enemySumIDs:
        name = sumIDToName(sumID)
        puuid = sumIDToPuuid(sumID)
        if queueType == 1:
            stats = puuidToRankedSolo(puuid)
            render(stats, name, puuid, SOLODUO)
        elif queueType == 2:
            stats = puuidToRankedFlex(puuid)
            render(stats, name, puuid, FLEX)
        

def queryByName(name):
    puuid = nameToPuuid(name)
    stats = puuidToRankedSolo(puuid)
    render(stats, name, puuid, SOLODUO)