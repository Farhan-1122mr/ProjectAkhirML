import socket
import os
import sys
from dump.data import Data
from constant import HEADERSIZE, BUFFER
import pickle

class Server:
    def __init__(self, address='127.0.0.1', port=5000) -> None:
        self.address = address
        self.port = port
        self.sock = None

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address, self.port))
        self.sock.listen(5)
        print("Server starts ...")

    def close_server(self):
        self.sock.close()

    def accept_connection(self):
        self.client, self.client_address = self.sock.accept()
        print(f"Connection from {self.client_address} has been established.")

    def run(self):
        self.start_server()
        self.accept_connection()
        
        full_msg = b''
        new_msg = True
        while True:
            msg = self.client.recv(BUFFER)
            if new_msg:
                print(msg[:HEADERSIZE])
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:
                data = pickle.loads(full_msg[HEADERSIZE:])
                print(self.client)
                print(self.client_address)

                file = open(data.filename, 'wb')
                file.write(data.file)

class Client:
    def __init__(self, address='127.0.0.1', port=5000) -> None:
        self.address = address
        self.port = port
        self.sock = None

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
    
    def close_client(self):
        self.sock.close()
        sys.exit(0)

    def send_data(self, filename):
        self.connect_to_server()
        fname = 'images/'+filename
        fsize = os.path.getsize(fname)
        rfile = b''
        with open(fname, 'rb') as file:
            while True:
                data = file.read()
                rfile += data
                if not data: break
        file.close()

        data_to_send = Data(rfile, fsize, filename)

        data_to_send = pickle.dumps(data_to_send)
        data_to_send = bytes(f"{len(data_to_send):<{HEADERSIZE}}", 'utf-8')+data_to_send
        print(int(data_to_send[:HEADERSIZE]))
        if self.sock.send(data_to_send):
            self.close_client()
