import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "shelter.json")
LOG_FILE = os.path.join(BASE_DIR, "shelter.log")

FIELDS = {
    1: ("shelter_name", "Shelter name"),
    2: ("leader", "Leader"),
    3: ("survivors", "Survivors"),
    4: ("food", "Food"),
    5: ("water", "Water"),
    6: ("barricade_health", "Barricade health"),
    7: ("radio_working", "Radio working"),
}

def clear_screen():
    """Clear terminal window"""
    os.system("cls" if os.name == "nt" else "clear")

def load_shelter():
    """Load shelter data from JSON file"""
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_shelter(data):
    """Save the shelter dictionary to JSON with indentation"""
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def log_change(field, old, new):
    """Append one timestamped change entry to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {field} changed from '{old}' to '{new}'\n"
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)

def radio_label(value):
    """Return working or not working for a boolean radio status"""
    return "Working" if value else "Not working"

def format_value(key, value):
    """Format a value for display"""
    return radio_label(value) if key == "radio_working" else value

def get_label(key):
    """Return the human-readable label for a field key"""
    for _number, (field_key, label) in FIELDS.items():
        if field_key == key:
            return label
    return key

def show_shelter(data):
    """Print all seven shelter fields with readable labels"""
    print("\nShelter Information")
    print("-------------------")
    for _number, (key, label) in FIELDS.items():
        print(f"{label}: {format_value(key, data[key])}")

def show_log():
    """Print the change log, or a message if it is missing or empty"""
    print("\nShelter Change Log")
    print("------------------")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            text = file.read()
        print(text.rstrip() if text.strip() else "No changes have been recorded yet.")
    except FileNotFoundError:
        print("No changes have been recorded yet.")

def read_whole_number(prompt, maximum=None):
    """Ask for a whole number, continues until valid"""
    while True:
        text = input(prompt).strip()
        clear_screen()
        if text.isdigit() and (maximum is None or int(text) <= maximum):
            return int(text)
        if maximum is None:
            print("Please enter a whole number of 0 or greater.")
        else:
            print(f"Please enter a whole number from 0 through {maximum}.")

def read_nonempty_text(prompt):
    """Ask for nonempty text. Reprompts until valid"""
    while True:
        text = input(prompt).strip()
        clear_screen()
        if text:
            return text
        print("Please enter some text.")

def read_yes_no(prompt):
    """Ask a yes/no question, returns true or false."""
    while True:
        answer = input(prompt).strip().lower()
        clear_screen()
        if answer == "yes":
            return True
        if answer == "no":
            return False
        print("Please enter yes or no.")

def ask_field_choice():
    """Show the field menu and return the chosen field key"""
    print("\nWhich value would you like to change?")
    for number, (_key, label) in FIELDS.items():
        print(f"{number}. {label}")
    try:
        choice = int(input("Choose a field: "))
    except ValueError:
        clear_screen()
        return None
    clear_screen()
    return FIELDS.get(choice, (None, None))[0]

def ask_new_value(key):
    """Prompt for a validated replacement value for the given field"""
    if key == "shelter_name":
        return read_nonempty_text("Enter the new shelter name: ")
    if key == "leader":
        return read_nonempty_text("Enter the new leader: ")
    if key == "barricade_health":
        return read_whole_number("Enter the new barricade health: ", maximum=100)
    if key == "radio_working":
        return read_yes_no("Is the radio working? (yes/no): ")
    return read_whole_number(f"Enter the new {get_label(key).lower()} total: ")

def change_value(data):
    """Picks a field, validates input, save, and log"""
    key = ask_field_choice()
    if key is None:
        print("Please choose a number between 1 and 7.")
        return
    label = get_label(key)
    old = data[key]
    print(f"Current {label.lower()}: {format_value(key, old)}")
    new = ask_new_value(key)
    if new == old:
        print("Nothing changed, so no log entry was added.")
        return
    data[key] = new
    save_shelter(data)
    log_change(key, format_value(key, old), format_value(key, new))
    print(f"{label} changed from {format_value(key, old)} to {format_value(key, new)}.")
    print("Shelter data saved. Change recorded in shelter.log.")

def run_menu(data):
    """Run the main menu loop until user quits"""
    while True:
        print("\nZombie Shelter Manager")
        print("1. View shelter information")
        print("2. Change a shelter value")
        print("3. View change log")
        print("4. Quit")
        choice = input("Choose an option: ").strip()
        clear_screen()
        if choice == "1":
            show_shelter(data)
        elif choice == "2":
            change_value(data)
        elif choice == "3":
            show_log()
        elif choice == "4":
            print("Exiting. Your changes have been saved.")
            return
        else:
            print("Invalid choice. Please enter a number 1-4.")

def main():
    """Load shelter data and start the menu"""
    clear_screen()
    data = load_shelter()
    if data is not None:
        run_menu(data)

if __name__ == "__main__":
    main()