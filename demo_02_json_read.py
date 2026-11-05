import json

try:
    with open("many_people.json", "r") as file:
        data = json.load(file)
    print(data)
except FileNotFoundError:
    print("JSON File not found")

# print out "osaka" and "pirate" from data
print(data[0]["name"] ,data[0]["job"] )

for record in data:
    print(record["name"], record["job"])

# print out misato's age
print(data[2]["age"])

