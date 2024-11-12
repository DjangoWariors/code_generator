import csv

from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.http import HttpResponse

from app.models import UniqueCode
import secrets
import string
import time
import logging

logger = logging.getLogger(__name__)


def create_batch_unique_codes(target_count=100000000, length=6, batch_size=1000, max_retries=5, brand=None,
                              code_batch=None):
    """Generate and insert a target number of unique codes into the database with an associated brand and code batch."""
    characters = string.ascii_uppercase + string.digits
    total_generated = 0

    while total_generated < target_count:
        codes = set()

        # Adjust batch_size to not exceed the target_count
        current_batch_size = min(batch_size, target_count - total_generated)

        # Step 1: Generate a batch of unique codes
        while len(codes) < current_batch_size:  # <--- Change made here
            code = ''.join(secrets.choice(characters) for _ in range(length))
            codes.add(code)

        # Step 2: Prepare batch for insertion, including the brand and code_batch
        unique_codes = [UniqueCode(unique_code=code, brand=brand, code_batch=code_batch) for code in codes]

        # Step 3: Attempt to insert batch into the database with retries
        retries = 0
        while retries < max_retries:
            try:
                with transaction.atomic():
                    UniqueCode.objects.bulk_create(unique_codes, ignore_conflicts=True)
                # Update count based on how many codes were actually saved
                total_generated += len(unique_codes)
                logger.info(f"Batch inserted successfully. Total generated: {total_generated}")
                break
            except IntegrityError:
                retries += 1
                logger.warning(f"Retrying batch due to IntegrityError (Attempt {retries}/{max_retries})")
                time.sleep(0.1)

        if retries == max_retries:
            logger.error("Max retries reached for current batch. Moving to the next batch.")


def export_unique_codes_to_csv(request, batch_size=1000000):
    """
    Export unique codes from the database into a CSV file with each column containing up to 10 lakh rows.
    """
    # Create the HTTP response with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unique_codes.csv"'

    writer = csv.writer(response)

    # Paginate the queryset in chunks of 'batch_size' rows
    paginator = Paginator(UniqueCode.objects.all().order_by('-id'), batch_size)
    num_pages = paginator.num_pages

    # Prepare to collect data for multiple columns
    columns_data = [[] for _ in range(num_pages)]

    # Iterate over each page and collect data into the corresponding column
    for page_number in range(1, num_pages + 1):
        page = paginator.page(page_number)
        column_index = (page_number - 1) % len(columns_data)
        for unique_code in page.object_list:
            columns_data[column_index].append(unique_code.unique_code)

    # Determine the maximum number of rows needed for the CSV file
    max_rows = max(len(column) for column in columns_data)

    # Write the header row with column names
    header = [f'Column {i + 1}' for i in range(len(columns_data))]
    writer.writerow(header)

    # Write rows into the CSV
    for row_index in range(max_rows):
        row = []
        for column in columns_data:
            if row_index < len(column):
                row.append(column[row_index])
            else:
                row.append('')
        writer.writerow(row)

    return response
