import pytest
from contactform.utils import GoogleSheet


def test_create_instance_with_valid_sheet_name_env(google_sheet_obj: GoogleSheet):
    google_sheet = google_sheet_obj
    # Assert
    assert isinstance(google_sheet, GoogleSheet)


def test_raises_error_with_invalid_or_missing_sheet_name_env():
    # Arrange
    sheet_name_env = "INVALID_SHEET_NAME"

    # Act & Assert
    with pytest.raises(Exception):
        GoogleSheet(sheet_name_env)


def test_get_last_row_index(google_sheet_obj: GoogleSheet):
    # Act
    last_row_index = google_sheet_obj.get_last_row()

    # Assert
    assert isinstance(last_row_index, int)


def test_add_new_row_with_valid_input(google_sheet_obj: GoogleSheet):
    # Arrange
    google_sheet = google_sheet_obj
    last_row_index = google_sheet.get_last_row()
    row_values = ["value1", "value2", "value3", "value4"]
    # Act
    google_sheet.add_new_row(row_values)
    new_row_index = google_sheet.get_last_row()
    # Assert
    assert new_row_index == last_row_index + 1


def test_add_multiple_new_rows_with_valid_input(google_sheet_obj: GoogleSheet):
    # Arrange
    google_sheet = google_sheet_obj
    row1_values = ["value1", "value2", "value3", "value4"]
    row2_values = ["value5", "value6", "value7", 'value8']
    last_row_index = google_sheet.get_last_row()
    # Act
    google_sheet.add_new_row(row1_values)
    google_sheet.add_new_row(row2_values)
    new_row_index = google_sheet.get_last_row()
    # Assert
    assert new_row_index == last_row_index + 2
