import csv

filepath = "employees.csv"

with open(filepath, "r", newline="") as file:
    content = csv.reader(file) # loads everything as csv reader object
    # print(content)
    # skip header row:
    next(content)
    for line in content:
        print(line)
        print(line[0]) # access a specific field of the csv

    # print the info with line numbers:
    for line_num, line in enumerate(content):
        print(f"{line_num}: {line}")