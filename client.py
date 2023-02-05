import socket
import threading
import config
import json

class Client:
    def __init__(self):
        self.HOST = config.HOST
        self.PORT = config.PORT
        self.FORMAT = config.FORMAT

        self.client = socket.socket()
        self.client.connect((self.HOST, self.PORT))

    def __receive(self):
        while True:
            data = self.client.recv(1024)
            print(data.decode(self.FORMAT))

    def __send(self):
        while True:
            msg = input()
            self.client.send(msg.encode(self.FORMAT))

    def __log_in(self):
        print("Log in")
        username = input('username: ')
        password = input('password: ')
        self.client.send(json.dumps(['log', username, password]).encode(self.FORMAT))

        return self.client.recv(1024).decode(self.FORMAT)

    def __registration(self):
        print("Registration")
        username = input('username: ')
        password = input('password: ')
        self.client.send(json.dumps(['reg', username, password]).encode(self.FORMAT))
        print("Success!")

    def start_client(self):
        if self.__log_in() == 'True':
            receive_thread = threading.Thread(target=self.__receive)
            send_thread = threading.Thread(target=self.__send)
            send_thread.start()
            receive_thread.start()
        else:
            self.__registration()
            self.start_client()


if __name__ == '__main__':
    Client().start_client()

