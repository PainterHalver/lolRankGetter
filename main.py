from getRank import getRank
from getGameState import getGameState, GameState
import os

try:
    print("Game state:", getGameState())
except:
    print("No game state found, please start the client")


while True:
    os.system("cls")
    print(f"Game state: {getGameState()}")
    if getGameState() == GameState.CHAMPSELECT:
        getRank(GameState.CHAMPSELECT)
    elif getGameState() == GameState.INPROGRESS:
        getRank(GameState.INPROGRESS)
    else:
        print("No suitable gamestate found")

    option = input("Press Enter to continue...")
