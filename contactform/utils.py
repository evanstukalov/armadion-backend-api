from gspread.spreadsheet import Worksheet
import itertools
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from armadion.settings import BASE_DIR

import logging

logger = logging.getLogger(__name__)

# Use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(BASE_DIR, 'credentials.json'), scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("Armadion")
worksheet = sheet.get_worksheet(0)

def get_last_row(worksheet: Worksheet) -> int:
    """
    Returns the index of the last row in the given worksheet.

    Args:
        worksheet (Worksheet): The worksheet to get the last row from.

    Returns:
        int: The index of the last row.
    """

    return len(worksheet.get_all_values())

def add_new_row(*rows: list, value: str = 'новая') -> None:
    """
    Add a new row to the worksheet with the given arguments.

    Args:
        *rows: Variable number of lists containing the values for the new row.
        value (str): The value to append to the new row.

    Returns:
        None
    """
    # Create a new row by combining the variable number of lists into a single list
    new_row = list(itertools.chain.from_iterable(rows))

    # Append the value to the new row
    new_row.append(value)

    # Get the index of the last row in the worksheet and increment it by 1 to determine the index of the new row
    last_row_index = get_last_row(worksheet) + 1

    # Insert the new row into the worksheet at the determined index, using the value input option "USER_ENTERED"
    worksheet.insert_row(new_row, last_row_index, value_input_option="USER_ENTERED")