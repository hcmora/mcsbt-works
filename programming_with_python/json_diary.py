import json
from datetime import datetime

# JSON file to store diary entries
diary_file = "diary.json"

# Load existing diary entries from JSON file


def load_diary() -> dict:
    try:
        with open(diary_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save updated diary entries back to JSON file


def save_diary(diary: dict) -> None:
    with open(diary_file, 'w') as f:
        json.dump(diary, f, indent=4)

# Add a new entry to the diary


def add_entry(date: str, title: str, content: str) -> None:
    diary = load_diary()
    if date not in diary:
        diary[date] = []
    diary[date].append({"title": title, "content": content})
    save_diary(diary)
    print("Entry added successfully.")

# View entries for a specific date


def view_entries(date: str) -> None:
    diary = load_diary()
    entries = diary.get(date, [])
    if entries:
        print(f"\nEntries for {date}:")
        for entry in entries:
            print(f"Title: {entry['title']}")
            print(f"Content: {entry['content']}\n")
    else:
        print(f"\nNo entries found for {date}.")

# Delete an entry by title for a specific date


def delete_entry(date: str, title: str) -> None:
    diary = load_diary()
    if date in diary:
        diary[date] = [entry for entry in diary[date] if entry['title'] != title]
        if not diary[date]:  # Remove the date if no entries remain
            del diary[date]
        save_diary(diary)
        print(f"Entry '{title}' deleted successfully.")
    else:
        print(f"\nNo entries found for {date}.")

# Main menu interface


def main_menu():
    while True:
        print("\nDiary Application Menu:")
        print("1. Add an entry")
        print("2. View entries for a specific date")
        print("3. Delete an entry by title for a specific date")
        print("4. Exit")

        choice = input("Please choose an option (1-4): ")

        if choice == "1" or "add" in choice.lower():
            date = input("Enter the date for the entry (YYYY-MM-DD): ")
            title = input("Enter the title of the entry: ")
            content = input("Enter the content of the entry: ")
            add_entry(date, title, content)

        elif choice == "2" or "view" in choice.lower():
            date = input("Enter the date to view entries (YYYY-MM-DD): ")
            view_entries(date)

        elif choice == "3" or "delete" in choice.lower():
            date = input(
                "Enter the date of the entry you want to delete (YYYY-MM-DD): ")
            view_entries(date)
            title = input("Enter the title of the entry you want to delete: ")
            delete_entry(date, title)
            print(f"\nThe entries for date {date} are:")
            view_entries(date)

        elif choice == "4" or "exit" in choice.lower():
            print("Exiting the diary application.")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 4.")


if __name__ == "__main__":
    main_menu()
