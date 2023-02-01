import socket
import threading
import config


class Client:
    def __init__(self):
        self.HOST = config.HOST
        self.PORT = config.PORT
        self.FORMAT = config.FORMAT

        self.s = socket.socket()
        self.s.connect((self.HOST, self.PORT))

    def __receive(self):
        while True:
            data = self.s.recv(1024)
            print(data.decode(self.FORMAT))

    def __send(self):
        while True:
            msg = input()
            self.s.send(msg.encode(self.FORMAT))

    def start_client(self):
        self.s.send(input('username: ').encode(self.FORMAT))

        receive_thread = threading.Thread(target=self.__receive)
        send_thread = threading.Thread(target=self.__send)
        send_thread.start()
        receive_thread.start()


if __name__ == '__main__':
    Client().start_client()

