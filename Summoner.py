from RankedStats import RankedStats
from api import call, BASE_URL
from MatchHistory import MatchHistory


class Summoner:
    accountId = 0
    name = ""
    puuid = ""
    summonerId = 0

    # rankedStats
    # matchHistory

    def __init__(self, name="", puuid="", summonerId=0):
        url = ""
        if name != "":
            url = f"{BASE_URL}/lol-summoner/v1/summoners?name={name}"
        elif puuid != "":
            url = f"{BASE_URL}/lol-summoner/v1/summoners-by-puuid-cached/{puuid}"
        elif summonerId != 0:
            url = f"{BASE_URL}/lol-summoner/v1/summoners/{summonerId}"

        self.__populateData(url)
        self.rankedStats = RankedStats(self.puuid)
        self.matchHistory = MatchHistory(self.puuid)

    def __populateData(self, url):
        data = call(url)
        self.name = data["displayName"]
        self.accountId = data["accountId"]
        self.puuid = data["puuid"]
        self.summonerId = data["summonerId"]

# painter = Summoner("PainterHalver")
# print(painter.rankedStats.RANKED_SOLO_5x5)
# print(painter.matchHistory.last20)

