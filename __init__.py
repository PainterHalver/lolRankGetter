from getRank import *

input("Press Enter to init...")
try:
    lobbyInit()
    input("Done! Press Enter when game starts to load...")
except:
    quit = input("Can't lobbyInit! Maybe get into a game lobby first? Press Enter to go to gameStartInit or type 'exit' to quit...")
    if quit == "exit":
        quit()

try:
    gameStartInit()
    input("The End! Press Enter to exit...")
except:
    input("Problem with gameStartInit! Press Enter to exit...")
    quit()