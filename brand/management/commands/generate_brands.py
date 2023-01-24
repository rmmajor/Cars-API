from django.core.management.base import BaseCommand
from brand.factories import BrandFactory

"""
This file implements manage.py console command: 
    python manage.py generate_brands <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = 'Generates records for Brand instance'

    def add_arguments(self, parser):
        parser.add_argument('count', action='store', nargs='+', type=int)

    def handle(self, *args, **options):

        count = options['count'][0]
        brand_records = BrandFactory.create_batch(count)
        return self.stdout.write("done")
