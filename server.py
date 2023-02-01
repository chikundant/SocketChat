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

    def __broadcast(self, data, sender):
        for user in self.users.keys():
            if user != sender:
                user.send(f"{self.users[user]}: {data.decode(self.FORMAT)}".encode(self.FORMAT))

    def __receive(self, client):
        try:
            while True:
                data = client.recv(1024)
                if client not in self.users:
                    self.__write_user({client: data.decode(self.FORMAT)})
                    continue
                if data:
                    self.__broadcast(data, client)
        except Exception as e:
            self.server.close()
            print("[SERVER CONNECTION CLOSED]")

    def start_server(self):
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


if __name__ == '__main__':
    ChatServer().start_server()
