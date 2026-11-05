"""
JSON (JavaScript Object Notaiton) is a popular format for storing structured data
It uses key-value pairs similar to: dictionaries in python

example:
{
    "name": "Osaka",
    "age": 18,
    "job": "Student"
}

to work with json in python you need to import json
"""

import json

# writing to json file:
person = {
    "name": "Osaka",
    "age": 18,
    "job": "Student"
}

file_path = "people.json"

with open(file_path, "w") as file:
    json.dump(person, file, indent=4)

print(f"JSON file ({file_path}) created successfully")

many_people = [
{
    "name": "Osaka",
    "age": 18,
    "job": "Student"
},
{
    "name": "Nami",
    "age": 35,
    "job": "Pirate"
},
{
    "name": "Misato",
    "age": 29,
    "job": "Commander"
}
]

file_path_new = "many_people.json"

with open("many_people.json", 'w') as file:
    json.dump(many_people,file,indent=4)