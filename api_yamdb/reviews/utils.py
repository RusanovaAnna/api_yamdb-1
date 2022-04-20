import csv
from sqlalchemy import create_engine, Table, MetaData

engine = create_engine('sqlite:///db.sqlite3')
metadata = MetaData()
reviews_genre = Table(
    'reviews_genre', metadata, autoload=True, autoload_with=engine)
insert_query = reviews_genre.insert()

with open('static/data/genre.csv', 'r', encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=",")
    engine.execute(
        insert_query,
        [{'id': row[0], 'name': row[1], 'slug': row[2]} for row in csv_reader])
