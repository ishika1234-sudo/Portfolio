import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO portfolio(title, content, link) VALUES (?,?,?)",
            ('second post', 'second post comment','https://www.github.com'))


connection.commit()
connection.close()
