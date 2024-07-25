from datetime import datetime

date_format = "%d-%m-%Y"  # Date format
CATEGORIES = {"I": "Income", "E": "Expense"}  # Categories for transactions

def get_date(prompt, allow_default=False):
    """Get date from user input"""
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)  # Return today's date if no input and allow_default is True

    try:
        valid_date = datetime.strptime(date_str, date_format)  # Validate the date format
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Date Format. Please enter the date in dd-mm-yyyy format")  # Handle invalid date format
        return get_date(prompt, allow_default)

def get_amount():
    """Get amount from user input"""
    try:
        amount = float(input("Enter the Amount: "))  # Get amount as float
        if amount == 0:
            raise ValueError("Amount must be a non-negative non-zero value")  # Validate amount
        return amount
    except ValueError as e:
        print(e)  # Handle invalid amount
        return get_amount()

def get_category():
    """Get category from user input"""
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]  # Return valid category
    
    print("Invalid Category. Please enter 'I' for income or 'E' for Expense.")  # Handle invalid category
    return get_category()

def get_description():
    """Get description from user input"""
    return input("Enter description (optional): ")  # Get optional description