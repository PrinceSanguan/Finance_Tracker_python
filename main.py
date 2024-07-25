import pandas as pd  # Importing the pandas library for data manipulation
import csv  # Importing the csv module for CSV file operations
from datetime import datetime  # Importing the datetime module for date operations
from data_entry import get_amount, get_category, get_date, get_description  # Importing functions from data_entry module
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

class CSV:
    CSV_FILE = "finance_data.csv"  # File name for storing financial data
    COLUMNS = ["date", "amount", "category", "description"]  # Columns for the CSV file
    FORMAT = "%d-%m-%Y"  # Date format

    @classmethod
    def initialize_csv(cls):
        """Initialize the CSV file with columns if it doesn't exist"""
        try:
            pd.read_csv(cls.CSV_FILE)  # Try to read the CSV file
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)  # Create a new DataFrame with the specified columns
            df.to_csv(cls.CSV_FILE, index=False)  # Save the DataFrame to CSV

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """Add a new entry to the CSV file"""
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)  # Create a CSV DictWriter
            writer.writerow(new_entry)  # Write the new entry to the CSV file
        print("Entry Added Successfully!!!!")  # Print success message

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Get transactions within a specified date range"""
        df = pd.read_csv(cls.CSV_FILE)  # Read the CSV file into a DataFrame
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)  # Convert date column to datetime
        start_date = datetime.strptime(start_date, cls.FORMAT)  # Parse start_date
        end_date = datetime.strptime(end_date, cls.FORMAT)  # Parse end_date

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)  # Create a mask for the date range
        filtered_df = df.loc[mask]  # Filter the DataFrame

        if filtered_df.empty:
            print('No transactions found in the given date range')  # Print message if no transactions found
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))  # Print transactions

            # Summary section
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()  # Calculate total income
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()  # Calculate total expense
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df  # Return the filtered DataFrame

def add():
    """Add a new transaction"""
    CSV.initialize_csv()  # Initialize the CSV file
    date = get_date("Enter the date of transaction (dd-mm-yyyy): or enter for today's date:", allow_default=True)  # Get date
    amount = get_amount()  # Get amount
    category = get_category()  # Get category
    description = get_description()  # Get description
    CSV.add_entry(date, amount, category, description)  # Add the entry to the CSV

def plot_transactions(df):
    """Plot transactions over time"""
    df.set_index("date", inplace=True)  # Set the date column as index
    
    # Resample income and expense data by day
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    # Plot the income and expenses
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """Main function to handle user interaction"""
    while True:
        print("\n1. Add a new Transaction")
        print("2. View transaction and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()  # Add a new transaction
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")  # Get start date
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")  # Get end date
            df = CSV.get_transactions(start_date, end_date)  # Get transactions within the date range
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)  # Plot transactions if user wants to see a plot
        elif choice == "3":
            print("Exiting.... ")
            break  # Exit the program
        else:
            print("Invalid choice. Enter 1, 2 or 3.")  # Handle invalid input

if __name__ == "__main__":
    main()  # Run the main function