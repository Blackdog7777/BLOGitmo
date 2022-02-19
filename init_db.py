import sqlite3


def init_db():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
                ('Title1', 'Content1', 'System')
                )

    cur.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
                ('Text2', 'Content2', 'System')
                )

    connection.commit()
    connection.close()
