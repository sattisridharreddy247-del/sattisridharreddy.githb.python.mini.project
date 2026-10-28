"""
Expense Tracker - Python Mini Project
-------------------------------------
Concepts used: functions, lists, dictionaries, loops, conditionals,
file handling (JSON), exception handling, string formatting, datetime.

Run:  python expense_tracker.py
"""

import json
import os
from datetime import date

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]


# ---------- Data handling ----------
def load_expenses():
    """Load expenses from the JSON file (empty list if none exists)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read data file. Starting fresh.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


# ---------- Input helpers ----------
def get_amount(prompt):
    """Keep asking until the user enters a positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(value, 2)
        except ValueError:
            print("Please enter a valid number.")


def choose_category():
    """Show categories and return the chosen one."""
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice, try again.")


# ---------- Features ----------
def add_expense(expenses):
    description = input("Description: ").strip() or "No description"
    amount = get_amount("Amount: ")
    category = choose_category()
    expenses.append({
        "date": str(date.today()),
        "description": description,
        "amount": amount,
        "category": category,
    })
    save_expenses(expenses)
    print(f"\nAdded: {description} - {amount:.2f} ({category})")


def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print(f"\n{'#':<4}{'Date':<12}{'Description':<22}{'Category':<15}{'Amount':>10}")
    print("-" * 63)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<4}{e['date']:<12}{e['description'][:20]:<22}"
              f"{e['category']:<15}{e['amount']:>10.2f}")
    print("-" * 63)
    print(f"{'TOTAL':<53}{sum(e['amount'] for e in expenses):>10.2f}")


def summary_by_category(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    grand_total = sum(totals.values())

    print("\nSpending by category")
    print("-" * 40)
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        percent = amt / grand_total * 100
        bar = "#" * int(percent // 5)
        print(f"{cat:<15}{amt:>9.2f}  {percent:5.1f}%  {bar}")
    print("-" * 40)
    print(f"{'Total':<15}{grand_total:>9.2f}")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    choice = input("\nEnter the # to delete (or press Enter to cancel): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(expenses):
        removed = expenses.pop(int(choice) - 1)
        save_expenses(expenses)
        print(f"Deleted: {removed['description']}")
    elif choice:
        print("Invalid number.")


# ---------- Main menu ----------
def main():
    expenses = load_expenses()
    actions = {
        "1": ("Add expense", add_expense),
        "2": ("View all expenses", view_expenses),
        "3": ("Summary by category", summary_by_category),
        "4": ("Delete an expense", delete_expense),
    }

    while True:
        print("\n===== EXPENSE TRACKER =====")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice][1](expenses)
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
