import requests
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

import json

gameFile = os.path.join(script_dir, "gameID.txt")
gameInfoFile = os.path.join(script_dir, "gameInfo.json")
coverFile = os.path.join(script_dir, "coverID.txt")
coverURL = os.path.join(script_dir, "coverURLFile.txt")


url = "https://api.igdb.com/v4/games/"
headers={"Client-ID":"4wosykh1ay6nekw5wm7snyvfujab25", "Authorization":"Bearer 67ynk7wndnr0fdw2owihpucvglids0"}
coversURL = "https://api.igdb.com/v4/covers/"

gameIdFile = open(gameFile, "r")
gameInformation = open(gameInfoFile, "a+")
coverIdFile = open(coverFile, "r")
coverURLFile = open(coverURL, "w")

#lines = gameIdFile.readlines()
#for line in lines:
 #   x = requests.post(url, data=line, headers=headers)
  #  gameInformation.writelines(x.text)

#gameInformation = open(gameInfoFile)
#data = json.load(gameInformation)
#all_games = []
#for game in data:
 #   cover = game.get('cover', 0)
  ##     coverIdFile.write(str(cover) + "\n")

urlLines = coverIdFile.readlines()
print(urlLines)
for line in urlLines:
    print(line)
    x = requests.post(coversURL, data=line, headers=headers)
    coverURLFile.writelines(x.text)