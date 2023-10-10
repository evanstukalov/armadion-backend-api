import logging

from gspread.spreadsheet import Worksheet
import itertools
import os
import environ

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from armadion.settings import BASE_DIR, env

logger = logging.getLogger(__name__)

env = environ.Env()
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class GoogleSheet:
    def __init__(self, sheet_name_env):
        logger.warning("Create a new instance of the GoogleSheet class")

        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials_path = os.path.join(BASE_DIR, 'credentials.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

        client = gspread.authorize(creds)

        sheet_name = env.str(sheet_name_env)
        self.sheet = client.open(sheet_name).get_worksheet(0)

    def get_last_row(self) -> int:
        """
        Returns the index of the last row in the given worksheet.

        Returns:
            int: The index of the last row.
        """
        last_row_index = len(self.sheet.get_all_values())
        return last_row_index


    def add_new_row(self, *rows: list) -> None:
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

        # Get the index of the last row in the worksheet and increment it by 1 to determine the index of the new row
        last_row_index = self.get_last_row() + 1

        # Insert the new row into the worksheet at the determined index, using the value input option "USER_ENTERED"
        self.sheet.insert_row(new_row, last_row_index, value_input_option="USER_ENTERED")