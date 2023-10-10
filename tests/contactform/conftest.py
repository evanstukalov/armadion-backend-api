import os

import pytest
@pytest.fixture
def google_sheet_obj():
    from contactform.utils import GoogleSheet
    return GoogleSheet("GOOGLE_SHEET_NAME")

