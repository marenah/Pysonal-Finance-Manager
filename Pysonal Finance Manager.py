import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('finance_manager.db')
c = conn.cursor()

# Create expenses table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, amount REAL, category TEXT)''')

# Function to record expense
def record_expense(amount, category):
    c.execute('''INSERT INTO expenses (amount, category)
                 VALUES (?, ?)''', (amount, category))
    conn.commit()

# Function to get total expenses by category
def get_total_expenses():
    c.execute('''SELECT category, SUM(amount) FROM expenses GROUP BY category''')
    results = c.fetchall()
    return results

# CLI -- Text and input
def main():
    print("Welcome to Personal Finance Manager")
    while True:
        print("\nChoose an option:")
        print("1. Record an Expense")
        print("2. View Total Expenses by Category")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            amount_str = input("Enter expense amount (with or without '$'): ")
            # Remove '$' if present in the input
            amount_str = amount_str.replace('$', '')
            # Convert amount to float
            amount = float(amount_str)
            category = input("Enter expense category: ")
            record_expense(amount, category)
            print("Expense recorded successfully.")
        elif choice == '2':
            results = get_total_expenses()
            if results:
                categories = [row[0] for row in results]
                expenses = [row[1] for row in results]
                labels = [f'{category}\n${expense:.2f} ({expense / sum(expenses) * 100:.1f}%)' for category, expense in zip(categories, expenses)]
                plt.pie(expenses, labels=labels, startangle=140)
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.title('Total Expenses by Category')
                plt.show()
            else:
                print("No expenses recorded.")
        elif choice == '3':
            # Clear the expenses table and close the connection
            c.execute('''DELETE FROM expenses''')
            conn.commit()
            conn.close()
            print("Database cleared. Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
