
from celery import shared_task

import logging

from contactform.utils import GoogleSheet

logger = logging.getLogger(__name__)


@shared_task()
def task_execute(data):
    """
    Execute a task to add a new row with the values from the serializer data.

    Args:
        data (dict): A dictionary containing the values for the new row.
    """
    try:
        sheet = GoogleSheet("GOOGLE_SHEET_NAME")

        sheet.add_new_row(list(data.values()))
        logger.warning(data)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
