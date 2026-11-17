import csv
import os

def main():
    base_dir = "CSV Practice"
    input_file = os.path.join(base_dir, "student_test_scores.csv")
    passed_file = os.path.join(base_dir, "passed.csv")
    failed_file = os.path.join(base_dir, "failed.csv")

    students = []

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Test Score"] = int(row["Test Score"])
            students.append(row)

    passed = [s for s in students if s["Test Score"] >= 70]
    failed = [s for s in students if s["Test Score"] < 70]

    fieldnames = reader.fieldnames
    for path, records in [(passed_file, passed), (failed_file, failed)]:
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    if students:
        top = max(students, key=lambda s: s["Test Score"])
        bottom = min(students, key=lambda s: s["Test Score"])
        average = sum(s["Test Score"] for s in students) / len(students)

        print(f"Highest score: {top['Student']} ({top['Test Score']})")
        print(f"Lowest score:  {bottom['Student']} ({bottom['Test Score']})")
        print(f"Average score: {average:.2f}")
    else:
        print("No student records found.")

if __name__ == "__main__":
    main()