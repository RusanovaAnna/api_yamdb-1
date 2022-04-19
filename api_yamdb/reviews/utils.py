import csv
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/genre_title.csv', 'r') as file:
    dr = csv.DictReader(file, delimiter=",")
    to_db = [(i['id'], i['genre_id'], i['title_id']) for i in dr]

cur.executemany(
    "INSERT INTO reviews_genretitle(id,genre_id,title_id) VALUES (?, ?, ?);",
    to_db)
con.commit()
con.close()
