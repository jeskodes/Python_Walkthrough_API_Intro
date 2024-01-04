# Settings needed to access spreadsheet data 

import gspread #importing gspread library 
from google.oauth2.service_account import Credentials # this is like specifying the file path 

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
    """
    while True:
        print("Please give sales for the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 18, 20, 50, 30, 20, 30\n")

        data_str = input("Enter your data here:") # User enters 6 numbers separated by commas
        print(f"The data you provided is {data_str}")

        sales_data = data_str.split(",") # the data entered is being collected as string - want a list of values. 
        print(sales_data)
        # The split() method returns the values as a list. We removed the string commmas and turn the string into a list. 

        # print(sales_data) # check the string is being returned as a list. This is to check - can be deleted. 
    
        if validate_data(sales_data):
            print("Valid data entered")
            break # calling the validate_data function and passing it the sales_data

        # put the validate_data function inside the get_sales_data function. 



# Want to validate data is exactly 6 numbers which we can convert to list and add to spreadsheet. 
# Create function to validate data and give error message if don't receive data we need for spreadsheet. 

def validate_data(values): #values is our sales data list
    """
    Inside the try/except statement, validates the data is exactly 6 numbers and converts the string 
    into a list of integers. 
    Raises ValueError if string cannot be converted into into
    """
    try:
        [int(value) for value in values]
        print(values) 

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

        
get_sales_data() # Calling the function 


"""
Explain str(e).lower():
Looking to match the default error message "invalid literal for int()"
Converts the error message to a lowercase string so matches. 
If this error message is given then will give custom error message. 
"""