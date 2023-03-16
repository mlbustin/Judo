"""
The 'Table' class is used to create a table object that represents the table in the database.
The table object is defined with columns that correspond to the columns in the database table.

The 'get_table' function uses the engine object to create a connection to the database,
and then executes a select query on the users table using the execute method of the connection object.
The results of the query are then fetched using the 'fetchall' method of the 'results' object.
"""
from DB import Database as db

connection_string = "mssql+pyodbc://localhost/Judo?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

user_db = db.Database(connection_string)

# Создадим нового пользователя
user_db.create_user("John Doe", 25)

# Получим информацию о пользователе
user = user_db.read_user(1)
print(user.name, user.age)

# Обновим информацию о пользователе
user_db.update_user(1, name="Jane Doe")
user = user_db.read_user(1)
print(user.name, user.age)

# Удалим пользователя
user_db.delete_user(1)
user = user_db.read_user(1) # вернет None, так как пользователь был удален
print(user)
