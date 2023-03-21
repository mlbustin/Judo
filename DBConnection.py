"""
The 'Table' class is used to create a table object that represents the table in the database.
The table object is defined with columns that correspond to the columns in the database table.

The 'get_table' function uses the engine object to create a connection to the database,
and then executes a select query on the users table using the execute method of the connection object.
The results of the query are then fetched using the 'fetchall' method of the 'results' object.
"""
from DB import Database as db

connection_string = "mssql+pyodbc://localhost/Judo?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

from DB.Database import UserDB

user_db = UserDB(connection_string)
user_db.create_user("John Doe", 25)
user_db.read_user(19)
user_db.update_user(19, name="Jane Jane")
user_db.delete_user(1)
