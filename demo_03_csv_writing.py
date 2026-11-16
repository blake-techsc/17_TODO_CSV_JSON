import csv

employees = [
    ["Name", "Age", "Job"],
    ["SpongeBob", 30, "Cook"],
    ["Patrick", 37, "Unemployed"],
    ["Sandy", 27, "Scientist"]
]

# write the 2D list to file
with open("employees.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # loop through 2D list and write each record to file
    for row in employees:
        writer.writerow(row)
    writer.writerow(["Julio", 99, "Athlete"])

print(f"CSV file written")

# write it all at once
with open("employees_2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(employees)