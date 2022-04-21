import csv

from django.core.management.base import BaseCommand
from sqlalchemy import MetaData, Table, create_engine

from api_yamdb.settings import DATABASES


class Command(BaseCommand):
    help = "Загружает в базу данных тестовые данные"

    def add_arguments(self, parser):
        parser.add_argument('engine_db', type=str, help=u'вид базы данных')

    def handle(self, *args, **kwargs):
        engine_db = kwargs['engine_db']
        db1 = DATABASES['default']['NAME']
        engine = create_engine(str(engine_db) + ':////' + str(db1))
        print(str(engine))
        metadata = MetaData()
        reviews_genre = Table(
            'reviews_genre', metadata, autoload=True, autoload_with=engine)
        insert_query = reviews_genre.insert()

        with open('static/data/genre.csv', 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=",")
            engine.execute(insert_query,
                           ([{'id': row[0], 'name': row[1], 'slug': row[2]}
                            for row in csv_reader]))
