from api import call, BASE_URL

class RankedStats:
    RANKED_SOLO_5x5 = {
        "tier": "",
        "division": "",
        "leaguePoints": 0,
        "wins": 0,
        "isProvisional": False
    }
    RANKED_FLEX_SR = {
        "tier": "",
        "division": "",
        "leaguePoints": 0,
        "wins": 0,
        "isProvisional": False
    }

    def __init__(self, puuid):
        self.__getRankedStatsByPuuid(puuid)

    def __getRankedStatsByPuuid(self, puuid):
        stats = call(f"{BASE_URL}/lol-ranked/v1/ranked-stats/{puuid}")
        self.RANKED_SOLO_5x5 = stats["queueMap"]["RANKED_SOLO_5x5"]
        self.RANKED_FLEX_SR = stats["queueMap"]["RANKED_FLEX_SR"]

# stat = rankedStats("9a9d9da3-391d-5b48-a869-3e94f614c957") # PainterHalver