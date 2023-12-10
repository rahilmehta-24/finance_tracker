# Version 0 #

import datetime

class Transaction:
    def __init__(self, category, description, amount, date=None):
        self.category = category
        self.description = description
        self.amount = amount
        self.date = date if date else datetime.datetime.now().date()

    def __str__(self):
        return f"{self.date}: {self.category} - {self.description} - {self.amount}"

class FinanceTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, category, description, amount):
        self.transactions.append(Transaction(category, description, amount))

    def show_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def total_expense(self):
        return sum(t.amount for t in self.transactions if t.amount < 0)

    def total_income(self):
        return sum(t.amount for t in self.transactions if t.amount > 0)

    def balance(self):
        return self.total_income() + self.total_expense()

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. Show Transactions")
        print("3. Total Income")
        print("4. Total Expense")
        print("5. Current Balance")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            category = input("Enter category (e.g., Food, Salary): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount (+ for income, - for expense): "))
            tracker.add_transaction(category, description, amount)
        elif choice == '2':
            tracker.show_transactions()
        elif choice == '3':
            print("Total Income: ", tracker.total_income())
        elif choice == '4':
            print("Total Expense: ", tracker.total_expense())
        elif choice == '5':
            print("Current Balance: ", tracker.balance())
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
