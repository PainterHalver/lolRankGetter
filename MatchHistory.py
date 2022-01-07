from api import call, BASE_URL

class MatchHistory:

    last20 = ""
    winCount = 0
    loseCount = 0

    def __init__(self, puuid):
        url = f"{BASE_URL}/lol-match-history/v1/products/lol/{puuid}/matches"
        data = call(url)
        self.games = data["games"]["games"]
        if len(self.games) < 20:
            return
        for i in range(20):
            if self.games[i]["gameDuration"] < 4.5 * 60:
                self.last20 = self.last20 + "R"
            else:
                if self.games[i]["participants"][0]["stats"]["win"]:
                    self.last20 = self.last20 + "W"
                    self.winCount = self.winCount + 1
                else:
                    self.last20 = self.last20 + "L"
                    self.loseCount = self.loseCount + 1

# m = MatchHistory("da89a31e-c708-59c6-8c2a-526547ec6460")