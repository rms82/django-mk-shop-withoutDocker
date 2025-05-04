import os
import csv

from django.core.management import BaseCommand

from order.management import data
from order.models import (
    Ostan, Shahrestan
)


class Command(BaseCommand):
    help = 'Generate all data'

    def add_arguments(self, parser):
        """initialize arguments"""
        pass

    def read_csv(self, path):
        with open(path, encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                print(row)
            return csv_reader

    def generate_ostan(self, path):
        with open(path, encoding='utf-8') as f:
            data = csv.DictReader(f)
            ostan_objs = [
                Ostan(
                    id=int(row.get('id')),
                    name=row.get('name'),
                    amar_code=row.get('amar_code')
                ) for row in data
            ]
            Ostan.objects.bulk_create(ostan_objs)
            print('Ostan Objects Created Successfully')

    def generate_shahrestan(self, path):
        with open(path, encoding='utf-8') as f:
            data = csv.DictReader(f)
            shahrestan_objs = [
                Shahrestan(
                    id=int(row.get('id')),
                    name=row.get('name'),
                    amar_code=row.get('amar_code'),
                    ostan_id=int(row.get('ostan'))
                ) for row in data
            ]
            Shahrestan.objects.bulk_create(shahrestan_objs)
            print('Shahrestan Objects Created Successfully')



 
    def handle(self, *args, **options):
        ostan_data_path = os.path.abspath(data.__file__).replace('__init__.py', 'ostan.csv')
        shahrestan_data_path = os.path.abspath(data.__file__).replace('__init__.py', 'shahrestan.csv')

        self.generate_ostan(ostan_data_path)
        self.generate_shahrestan(shahrestan_data_path)

        self.stdout.write(
            self.style.SUCCESS('Data generated successfully.')
        )
