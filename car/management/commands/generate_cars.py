from django.core.management.base import BaseCommand
from car.factories import CarFactory

"""
This file implements manage.py console command: 
    python manage.py generate_models <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = 'Generates records for Car instance'

    def add_arguments(self, parser):
        parser.add_argument('count', action='store', nargs='+', type=int)

    def handle(self, *args, **options):

        count = options['count'][0]
        car_records = CarFactory.create_batch(count)
        return self.stdout.write("done")
