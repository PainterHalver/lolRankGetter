from src import getRank
from src import getGameState

try:
    print("Game state:", getGameState.getGameState())
except:
    print("No game state found, please start the client")
print("1. In champ select")
print("2. Game started")
print("3. Exit")

while True:
    option = int(input("Your option: "))
    if option == 1:
        try:
            getRank.lobbyInit()
            print("Done!")
        except:
            print("Can't lobbyInit! Maybe you're not in a game lobby?")
            

    if option == 2:
        try:
            getRank.gameStartInit()
            print("Done!")
        except:
            print("Problem with gameStartInit! Maybe game hasn't started yet?")

    if option == 3:
        break
quit()