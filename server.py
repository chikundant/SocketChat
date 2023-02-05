import socket
import datetime
import threading
import json
import config


class ChatServer:
    def __init__(self):
        self.HOST = config.HOST
        self.PORT = config.PORT
        self.FORMAT = config.FORMAT

        self.server = socket.socket()
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()

        self.users = {}
        self.user_data = []

    def __broadcast(self, data, sender):
        for user in self.users.keys():
            if user != sender:
                user.send(f"{self.users[sender]}: {data.decode(self.FORMAT)}".encode(self.FORMAT))

    def __log_in(self, data, client):

        if data[0] == 'reg':
            with open('users.json', 'w') as f:
                self.user_data.append({"username": data[1], "password": data[2]})
                json.dump(self.user_data, f)
            self.__write_user({client: data[1]})
        if data[0] == 'log':
            for user in self.user_data:
                if user['username'] == data[1] and user['password'] == data[2]:
                    self.__write_user({client: data[1]})
                    client.send('True'.encode(self.FORMAT))
                    return
            client.send('False'.encode(self.FORMAT))

    def __receive(self, client):
        try:
            while True:
                data = client.recv(1024)
                try:
                    self.__log_in(json.loads(data), client)
                except:
                    if data:
                         self.__broadcast(data, client)
        except Exception as e:
            self.server.close()
            print("[SERVER CONNECTION CLOSED]")

    def start_server(self):
        self.load()
        print('[SERVER IS WORKING]')
        print(f"[{datetime.datetime.now()}]")
        try:
            while True:
                client, addr = self.server.accept()
                print(f"[NEW CONNECTION] {addr}")
                receive_thread = threading.Thread(target=self.__receive, args=(client,))
                receive_thread.start()
        except KeyboardInterrupt as e:
            print(e)
            self.server.close()
            print("[SERVER CONNECTION CLOSED]")

    def __write_user(self, user: {}):
        self.users.update(user)

    def load(self):
        try:
            with open('users.json', 'r') as f:
                data = f.read()
                self.user_data = json.loads(data)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ChatServer().start_server()
