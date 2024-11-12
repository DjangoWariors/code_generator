# myapp/management/commands/generate_unique_codes.py
from django.core.management.base import BaseCommand
import time
from app.models import UniqueCode
from app.views import create_batch_unique_codes


class Command(BaseCommand):
    help = 'Generate and insert unique codes into the database'

    def handle(self, *args, **options):
        target_count = 90969
        brand = "GTR"
        code_batch = "Batch002"

        # Initial batch generation
        create_batch_unique_codes(target_count=target_count, batch_size=1000, brand=brand, code_batch=code_batch)

        # Get the initial count of generated codes
        count = UniqueCode.objects.filter(code_batch=code_batch, brand=brand).count()

        # Loop until the count reaches the target
        while count < target_count:
            pending_count = target_count - count
            if pending_count > 0:
                # Generate the next batch of codes
                create_batch_unique_codes(target_count=pending_count, batch_size=1000, brand=brand,
                                          code_batch=code_batch)

                # Update the count after each batch generation
                print('sleep start')
                time.sleep(10)
                count = UniqueCode.objects.filter(code_batch=code_batch, brand=brand).count()

        self.stdout.write(self.style.SUCCESS('Successfully generated unique codes.'))

