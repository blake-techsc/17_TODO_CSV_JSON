# load the rick and morty file
# filter (use filter) the list of results into a new list with only alive characters
# write new list to rick_and_morty_alive.json file

import json

with open("rick_and_morty.json", "r") as file:
    data = json.load(file)
 
alive = list(filter(lambda x :  x["status"] == "Alive", data["results"]))
 
with open("alive_characters.json","w") as file:
    json.dump(alive, file, indent = 4)