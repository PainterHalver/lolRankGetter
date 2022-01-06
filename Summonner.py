from RankedStats import RankedStats
from api import call, BASE_URL


class Summonner:
    accountId = 0
    name = ""
    puuid = ""
    summonerId = 0

    # rankedStats

    def __init__(self, name="", puuid="", summonnerId=0):
        url = ""
        if (name != ""):
            url = f"{BASE_URL}/lol-summoner/v1/summoners?name={name}"
        elif (puuid != ""):
            url = f"{BASE_URL}/lol-summoner/v1/summoners-by-puuid-cached/{puuid}"
        elif (summonnerId != 0):
            url = f"{BASE_URL}/lol-summoner/v1/summoners/{summonnerId}"

        self.__populateData(url)
        self.rankedStats = RankedStats(self.puuid)

    def __populateData(self, url):
        data = call(url)
        self.name = data["displayName"]
        self.accountId = data["accountId"]
        self.puuid = data["puuid"]
        self.summonerId = data["summonerId"]

# painter = Summonner("PainterHalver")
# print(painter.rankedStats.RANKED_SOLO_5x5)

