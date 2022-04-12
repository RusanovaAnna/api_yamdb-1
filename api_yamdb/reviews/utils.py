import csv
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/users.csv', 'r') as file:
    dr = csv.DictReader(file, delimiter=",")
    to_db = [(i['id'], i['username'], i['email'], i['role'], i['bio'], i['first_name'], i['last_name'], i['password'], i['is_superuser'], i['is_staff'], i['is_active'], i['date_joined']) for i in dr]

cur.executemany(
    "INSERT INTO reviews_user (id, username, email, role, bio, first_name, last_name, password, is_superuser, is_staff, is_active, date_joined) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
