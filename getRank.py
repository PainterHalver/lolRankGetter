import base64
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GET AND PARSE THE 'LOCKFILE'
try:
    file = open("D:/LMHT/32787/LeagueClient/lockfile")
except:
    input("'lockfile' not found! Maybe open the game first? Press Enter to exit...")


lockfile = file.readline().split(":")

port = lockfile[2]
username = 'riot'
password = lockfile[3]

# ENCODE TO base64 AUTH CODE
message = f"{username}:{password}"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
authCode = base64_bytes.decode('ascii')

# NAME TO PUUID CODE
def nameToPuuid(name):
    nameToPuuidUrl = f"https://127.0.0.1:{port}/lol-summoner/v1/summoners?name={name}"
    x = requests.get(nameToPuuidUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    puuid = y["puuid"]
    return puuid

# SUMID TO PUUID CODE
def sumIDToPuuid(sumID):
    sumIDToPuuidUrl = f"https://127.0.0.1:{port}/lol-summoner/v1/summoners/{sumID}"
    x = requests.get(sumIDToPuuidUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    puuid = y["puuid"]
    return puuid

# SUMID TO NAME
def sumIDToName(sumID):
    sumIDToNameUrl = f"https://127.0.0.1:{port}/lol-summoner/v1/summoners/{sumID}"
    x = requests.get(sumIDToNameUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    name = y["displayName"]
    return name

# NAME TO SUMID
def nameToSumID(name):
    nameToSumIDUrl = f"https://127.0.0.1:{port}/lol-summoner/v1/summoners?name={name}"
    x = requests.get(nameToSumIDUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    sumID = y["summonerId"]
    return sumID

# PUUID TO RANKED INFO
def puuidToRankedSolo(puuid):
    puuidToRankedSoloUrl = f"https://127.0.0.1:{port}/lol-ranked/v1/ranked-stats/{puuid}"
    x = requests.get(puuidToRankedSoloUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    soloStats = (y["queueMap"]["RANKED_SOLO_5x5"])
    return soloStats


# def getRankedSolo(name):
#     puuid = nameToPuuid(name)
#     soloStats = puuidToRankedSolo(puuid)
#     tier = soloStats["tier"]
#     division = soloStats["division"]
#     lp = soloStats["leaguePoints"]
#     point = "point"
#     points = "points"
#     print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}")

# GET SUMID IN LOBBY
allySumIDs = []
def getAllAllySumID():
    getAllSumIDUrl = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
    x = requests.get(getAllSumIDUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    myTeam = y["myTeam"]
    global allySumIDs
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
        point = "point"
        points = "points"
        print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}")

input("Press Enter to init...")
try:
    lobbyInit()
    input("Done! Press Enter when game starts to load...")
except:
    quit = input("Can't lobbyInit! Maybe get into a game lobby first? Press Enter to go to gameStartInit or type 'exit' to quit...")
    if quit == "exit":
        quit()


# GET ENEMY "summonerInternalName" when game starts loading
def filterAllySumIDs(variable):
    global allySumIDs
    if (variable in allySumIDs):
        return False
    else:
        return True

def getEnemySumIDs():
    getEnemyNameUrl = f"https://127.0.0.1:{port}/lol-gameflow/v1/session"
    x = requests.get(getEnemyNameUrl, headers={"Authorization": f"Basic {authCode}"}, verify=False)
    y = json.loads(x.text)
    allPlayers= y["gameData"]["playerChampionSelections"]
    allSumIDs = []
    for i in allPlayers:
        sumID = nameToSumID(i["summonerInternalName"])
        allSumIDs.append(sumID)
    enemySumIDs = filter(filterAllySumIDs, allSumIDs)
    return enemySumIDs

def gameStartInit():
    for sumID in getEnemySumIDs():
        name = sumIDToName(sumID)
        puuid = sumIDToPuuid(sumID)
        soloStats = puuidToRankedSolo(puuid)
        tier = soloStats["tier"]
        division = soloStats["division"]
        lp = soloStats["leaguePoints"]
        point = "point"
        points = "points"
        print(f"{name}: {tier} {division} {lp} {points if lp != 1 else point}")

try:
    gameStartInit()
    input("The End! Press Enter to exit...")
except:
    input("Problem with gameStartInit! Press Enter to exit...")
    quit()