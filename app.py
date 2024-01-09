# Settings needed to access spreadsheet data 

import gspread #importing gspread library 
from google.oauth2.service_account import Credentials # this is like specifying the file path 
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Set scope. The scope lists the APIs that the program should access in order to run.
# In Python constant variable names are written in capitals. 

# The below are variables
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

# Check can access data 
# data = sales.get_all_values()
# print(data)

def get_sales_data(): 
    """
    Get sales data input from user
    While loop to continually request data of 6 numbers separated by commas. 
    Break when receive required data. 
    """
    while True:
        print("\nPlease give sales for the last market\n")
        print("Data should be six numbers, separated by commas\n")
        print("Example: 18, 20, 50, 30, 20, 30\n")

        data_str = input("Enter your data here: ") # User enters 6 numbers separated by commas
        print(f"\nThe data you provided is {data_str}")

        sales_data = data_str.split(",") # the data entered is being collected as string - want a list of values. 
        # print(sales_data)
        # The split() method returns the values as a list. We removed the string commmas and turn the string into a list. 

        # print(sales_data) # check the string is being returned as a list. This is to check - can be deleted. 
    
        if validate_data(sales_data):
            print("Figures added!")
            break # calling the validate_data function and passing it the sales_data

        # put the validate_data function inside the get_sales_data function. 

    return sales_data #this is the data returned from the get_sales_data function - need a place to put it. 

# Want to validate data is exactly 6 numbers which we can convert to list and add to spreadsheet. 
# Create function to validate data and give error message if don't receive data we need for spreadsheet. 

def validate_data(values): #values is our sales data list
    """
    Inside the try/except statement, validates the data is exactly 6 numbers and converts the string 
    into a list of integers. 
    Raises ValueError if string cannot be converted into int
    """
    try:
        values = [int(value) for value in values]
        # print(values) 

        if len(values) != 6: 
            raise ValueError(
                f"Please provide 6 values, you provided {len(values)}"
             )

    except ValueError as e: 
        if "invalid literal for int()" in str(e).lower():
            print("Invalid data: Please enter numbers only, not letters.")
        else: 
            print(f"Invalid data: {e}, please try again\n")
        return False
    
    return True

# def update_sales_worksheet(data):
#     """
#     Create function to add data input into spreadsheet
#     To create new row of data in spreadsheet
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales") # Add variable to access worksheet - specifically "sales" sheet. 
#     sales_worksheet.append_row(data) # Use append_row() method to add a row to spreadsheet with new data. 
#     print("Success! Data has been added!\n")


# def update_surplus_worksheet(data):
#     """
#     Create function to add calculated surplus data input into spreadsheet
#     To create new row of surplus data in spreadsheet
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus") # Add variable to access worksheet - specifically "sales" sheet. 
#     surplus_worksheet.append_row(data) # Use append_row() method to add a row to spreadsheet with new data. 
#     print("Success! Surplus stock has been saved!\n")

def update_worksheet(data, worksheet):
    """
    Two arguments, data and which worksheet to update
    Receives the integers to to be updated. 
    Updates relevant worksheet (sales or surplus)
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"Sucess! {worksheet} worksheet updated.\n")


def calculate_sales_data(sales_row): 
    """
    Function to compare sales vs stock - the surplus. 
    The surplus is the number of sales - the stock for that day. 
    Negative = extra sandwiches made
    Positive = sandwiches left over and thrown away
    Zip() method loops through more than one list at one time. 
    """
    print("Calculating surplus stock...\n")
    stock = SHEET.worksheet("stock").get_all_values() # Get stock data and put into variable called stock.
    # pprint(stock) 
    stock_row = stock[-1] # Variable to store last row in list of stock data. 

    surplus_stock = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_stock.append(surplus)

    return surplus_stock

def get_last_five_entries():
    """
    Get last 5 days worth of sales from spreadsheet
    Get columns and return as list of lists. 
    """
    sales = SHEET.worksheet('sales') # variable to get data
    # column = sales.col_values(3) # Use col_values() method to ask for column
    # print(column) # test if function working so far. Comment out call to main function. 

    columns = [] # create empty list 
    for ind in range(1, 7): # ind variable gets last 5 entries in column
        # print(ind)
        column = sales.col_values(ind) # Create column variable use col_values method and pass ind variable
        columns.append(column) # append column list to columns ?variable
    pprint(columns) # pprint(pretty print) prints out data that looks prettier/more readable for humans


def main(): 
    """
    In Python wrap all functions in main function. 
    Needs to be called below where it is defined.
    """      
    data = get_sales_data() # Calling the function. Put the data returned from the function in varialbe called "data"
    
    # print(data) # Print data to check working should look like: ['1', ' 2', ' 3', '4', ' 5', '6'] in terminal. 

    sales_data = [int(num) for num in data] # Create variable sales_data where convert and store list into integers. 
    # Using list comprehension - could use a for loop. 

    update_worksheet(sales_data, 'sales') # Calling function at end to update sales worksheet. Passing it sales_data variable. 

    new_surplus_stock = calculate_sales_data(sales_data) # Calling Function to calculate surplus stock. 
    # print(new_surplus_stock)

    update_worksheet(new_surplus_stock, 'surplus') # calling function to update surplus sheet with new data. 

print("\nWelcome to Love Sandwiches Data Automation") # This is the first statement that will print before other functions called. 
# main()

get_last_five_entries()


"""
Explain str(e).lower():
Looking to match the default error message "invalid literal for int()"
Converts the error message to a lowercase string so matches. 
If this error message is given then will give custom error message. 

Iterate over last list in stock data - create variable to store in then use list comprehension:
[sublist for sublist in stock][-1]
In this code, the list comprehension [sublist for sublist in data] creates a new list containing
all the sublists in the original data. 
The [-1] index then selects the last element (last sublist) in this new list.
"""