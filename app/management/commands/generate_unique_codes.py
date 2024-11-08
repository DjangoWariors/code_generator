# myapp/management/commands/generate_unique_codes.py
from django.core.management.base import BaseCommand

from app.views import create_batch_unique_codes


class Command(BaseCommand):
    help = 'Generate and insert unique codes into the database'

    def handle(self, *args, **options):
        create_batch_unique_codes(target_count=2095, batch_size=1000, brand="ETR", code_batch="Batch001")
        self.stdout.write(self.style.SUCCESS('Successfully generated unique codes.'))
