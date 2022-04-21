import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre


class Command(BaseCommand):
    help = "Загружает в базу данных тестовые данные"

    def add_arguments(self, parser):
        parser.add_argument(
            'table', type=str, nargs='*', help=u'таблица', default='')

    def handle(self, *args, **kwargs):
        tables = kwargs['table']
        if not tables:
            tables = ['genre', 'category']

        for table in tables:
            if table == 'genre':
                value = 'genre'
                model = Genre
            if table == 'category':
                value = 'category'
                model = Category

            with open(f'static/data/{value}.csv',
                      'r', encoding="utf-8") as file:
                csv_reader = csv.reader(file, delimiter=",")
                for row in csv_reader:
                    model.objects.create(id=row[0], name=row[1], slug=row[2])
