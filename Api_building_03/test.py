# this is to see the working of sql_lite and python
import sqlite3

# opening connection to connect with sqlite. Here 'data.db' is our database. Sqlite is lite and store in file.
connection = sqlite3.connect('data.db')

# This allow to select and start things. Ex:- cursor start from top, it will also run the query and store the result
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

# running the query
cursor.execute(create_table)

# storing single user
user = (1, 'Jose', 'asd')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# storing multiple users
users = [
    (2, 'anne', 'asd'),
    (3, 'rolf', 'jkl')
]
cursor.executemany(insert_query, users)

# fetching data from database
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# telling connection to save the data
connection.commit()

connection.close()
