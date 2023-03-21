import socket
from DB import Database as db

connection_string = "mssql+pyodbc://localhost/Judo?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connection, self.address = None, None
        self.database = db.UserDB(connection_string)

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.connection, self.address = self.socket.accept()

        while True:
            try:
                data = self.connection.recv(1024)

                if not data:
                    break

                data = data.decode('utf-8')
                command = data.split(',')

                print(f'Received command: {data}, from {self.address}')

                if command[0] == 'exit':
                    self.connection.close()
                    self.socket.close()
                    break
                elif command[0] == 'u_create':
                    if len(command) == 4:
                        self.database.create_user(command[1], command[2], command[3])
                elif command[0] == 'u_delete':
                    if len(command) == 2:
                        self.database.delete_user(command[1])
                elif command[0] == 'u_get':
                    if len(command) == 2:
                        user = self.database.read_user(command[1])
                        self.connection.sendall([user.name.encode('utf-8'),
                                                 user.age.encode('utf-8'),
                                                 user.password.encode('utf-8')])
                elif command[0] == 'u_list':
                    pass
                elif command[0] == 'u_update':
                    if len(command) == 4:
                        self.database.update_user(command[1], command[2], command[3])

            except socket.timeout:
                print(f'Connection to {self.address} timed out')


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data.encode('utf-8'))
