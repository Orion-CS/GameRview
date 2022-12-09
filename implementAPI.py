import requests
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

gameFile = os.path.join(script_dir, "gameID.txt")
gameInfoFile = os.path.join(script_dir, "gameInfo.txt")

url = "https://api.igdb.com/v4/games/"
headers={"Client-ID":"4wosykh1ay6nekw5wm7snyvfujab25", "Authorization":"Bearer 67ynk7wndnr0fdw2owihpucvglids0"}

gameIdFile = open(gameFile, "r")
gameInformation = open(gameInfoFile, "a+")

lines = gameIdFile.readlines()
for line in lines:
    x = requests.post(url, data=line, headers=headers)
    print(x.text)
    gameInformation.writelines(x.text)
