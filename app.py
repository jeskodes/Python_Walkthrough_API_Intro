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
data = sales.get_all_values()
print(data)