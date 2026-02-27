import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

DATA_FILE = "data.csv"

# Initialize storage file
def initialize_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "type", "category", "amount"])
        print("Created data.csv for storage.\n")

# Add Entry
def add_entry():
    entry_type = input("Enter type (income/expense): ").lower()
    date = input("Enter date (YYYY7-MM-DD): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))

    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, entry_type, category, amount])

    print("\n✔ Entry added successfully!\n")

# View All Entries
def view_entries():
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        print("\nNo records found!\n")
        return
    print("\n=== All Entries ===")
    print(df)
    print()

# Monthly Summary
def monthly_summary():
    month = input("Enter month (1-12): ")
    year = input("Enter year (YYYY): ")

    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    filtered = df[(df["date"].dt.month == int(month)) & (df["date"].dt.year == int(year))]

    if filtered.empty:
        print("\nNo data found for this month.\n")
        return

    income = filtered[filtered["type"] == "income"]["amount"].sum()
    expense = filtered[filtered["type"] == "expense"]["amount"].sum()
    balance = income - expense

    print("\n=== Monthly Summary ===")
    print(f"Total Income: ₹{income}")
    print(f"Total Expense: ₹{expense}")
    print(f"Net Balance: ₹{balance}\n")

# Export to Excel
def export_excel():
    df = pd.read_csv(DATA_FILE)
    df.to_excel("expense_report.xlsx", index=False)
    print("\n✔ Exported to expense_report.xlsx\n")

# Generate Monthly Chart
def generate_chart():
    month = input("Enter month (1-12): ")
    year = input("Enter year (YYYY): ")

    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    filtered = df[(df["date"].dt.month == int(month)) & (df["date"].dt.year == int(year))]

    if filtered.empty:
        print("\nNo data to generate chart.\n")
        return

    category_sum = filtered.groupby("category")["amount"].sum()

    plt.figure(figsize=(6, 6))
    plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%")
    plt.title(f"Expense Breakdown - {month}/{year}")
    plt.savefig("expense_chart.png")
    plt.close()

    print("\n✔ Chart saved as expense_chart.png\n")

def edit_entry():
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("\nNo entries to edit.\n")
        return

    print("\n=== Existing Entries ===")
    print(df.reset_index())   # show entries with index
    print()

    try:
        index_to_edit = int(input("Enter the index of the entry to edit: "))
        if index_to_edit not in df.index:
            print("❌ Invalid index!\n")
            return
    except ValueError:
        print("❌ Please enter a valid number!\n")
        return

    # Show chosen entry
    print("\nSelected Entry:")
    print(df.loc[index_to_edit])
    print()

    # Input new values (Enter blank to keep old value)
    new_date = input(f"Enter new date (YYYY-MM-DD) or press Enter to keep ({df.loc[index_to_edit, 'date']}): ")
    new_type = input(f"Enter new type (income/expense) or press Enter to keep ({df.loc[index_to_edit, 'type']}): ")
    new_category = input(f"Enter new category or press Enter to keep ({df.loc[index_to_edit, 'category']}): ")
    new_amount = input(f"Enter new amount or press Enter to keep ({df.loc[index_to_edit, 'amount']}): ")

    # Update only changed fields
    if new_date:
        df.loc[index_to_edit, 'date'] = new_date
    if new_type:
        df.loc[index_to_edit, 'type'] = new_type
    if new_category:
        df.loc[index_to_edit, 'category'] = new_category
    if new_amount:
        df.loc[index_to_edit, 'amount'] = float(new_amount)

    # Save file
    df.to_csv(DATA_FILE, index=False)

    print("\n✔ Entry updated successfully!\n")

# Menu Loop
def main():
    initialize_file()

    while True:
        print("==== Expense Tracker CLI ====")
        print("1. Add Entry")
        print("2. View All Entries")
        print("3. Monthly Summary")
        print("4. Export to Excel")
        print("5. Generate Monthly Chart")
        print("6. Edit Entry")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            export_excel()
        elif choice == "5":
            generate_chart()
        elif choice == "6":
            edit_entry()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.\n")

if __name__ == "__main__":
    main()