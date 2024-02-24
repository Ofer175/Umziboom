import socket
import threading
import random
from client_protocol import ClientProtocol
import queue


class ClientCom:
    """
    client communication
    """

    def __init__(self, server_ip, port, msg_q, encrypt):
        """
        initializing parameters and creating communication object
        :param server_ip: server ip
        :param port: port of communication
        :param msg_q: queue for messages
        :param encrypt: for encrypting and decrypting
        """
        self.running = True
        self.socket = None     # server socket
        self.server_ip = server_ip
        self.port = port
        self.msg_q = msg_q
        self.encrypt = encrypt

        # calling main_loop thread
        threading.Thread(target=self._main_loop, daemon=True).start()

    def _main_loop(self):
        """
        creating communication with server, exchanging keys with server and starting to get data from server
        :return: None
        """
        self.socket = socket.socket()
        try:
            self.socket.connect((self.server_ip, self.port))
        except Exception as e:
            print("client_comm - _main_loop1. " + str(e))
        else:
            if self.port == 2000:
                # calling _diffie() thread to exchange key with client
                key = self._diffie()
                # putting key in encryption object
                self.encrypt.add_key(key)

            while self.running:
                try:
                    # receiving data from server
                    len_data = self.socket.recv(5).decode()
                    data = self.socket.recv(int(len_data))
                    # decrypting data
                    data = self.encrypt.decrypt(data).decode()
                    if data[:2] == '15' or data[:2] == '25':  # if receive file
                        proto = int(data[:2])  # message protocol
                        file_name = data[2:]  # file name

                        # receiving starting point
                        data_len = self.socket.recv(5).decode()
                        start_time = self.socket.recv(int(data_len))
                        # decrypting data
                        start_time = self.encrypt.decrypt(start_time).decode()
                        start_time = start_time[2:]  # removing protocol
                        print(f'start time - {start_time}')

                        # receiving volume
                        data_len = self.socket.recv(5).decode()
                        volume = self.socket.recv(int(data_len))
                        # decrypting data
                        volume = self.encrypt.decrypt(volume).decode()
                        volume = volume[2:]  # removing protocol
                        print(f'volume - {volume}')

                        # receiving file
                        data = self.recv_file(file_name, start_time, volume, proto)
                except Exception as e:
                    print('ClientComm - main_loop ', e)
                    self.msg_q.put("exit")  # to end main client code
                    break
                else:
                    if type(data) == str:  # if not receive file
                        data = ClientProtocol.unpack(data)
                    self.msg_q.put(data)
        self.socket.close()

    def _diffie(self):
        """
        exchanging key with client using Diffie Hellman protocol
        :param client: client socket
        :param addr: ip address of client
        :return: the encryption key
        """
        key = -1
        p = 5195977
        g = 35125

        private_b = random.randint(1, 9999)  # generating random private number
        B = (g ** private_b) % p  # number to exchange with client

        # sending B and receiving A
        try:
            # sending B
            message = str(B)
            self.socket.send((str(len(message)) + message).encode())

            # receiving B
            length = self.socket.recv(1).decode()  # getting message length
            A = int(self.socket.recv(int(length)).decode())

        except Exception as e:
            print('ClientComm - _diffie ', e)

        else:
            # calculating key
            key = (A ** private_b) % p
            print(f'key-{key}')
        return str(key)

    def send(self, msg):
        """
        sending messages to server
        :param msg: message to send
        :return: None
        """
        try:
            enc = self.encrypt.encrypt(msg)
            # sending length
            self.socket.send(str(len(enc)).zfill(5).encode())
            # sending encrypted message
            self.socket.send(enc)
        except Exception as e:
            print('ClientCom send - ', e)

    def send_file(self, file_path):
        """
        sending file to server
        :param file_path: file path
        :return: None
        """
        # getting file
        with open(file_path, 'rb') as strip:
            file = strip.read()
        enc = self.encrypt.encrypt(file)

        length = str(len(enc)).zfill(8)
        print(f'length1 - {length}')
        try:
            self.socket.send(str(len(enc)).zfill(8).encode())   # sending file length
        except Exception as e:
            print('ClientCom send_file - ', e)
        else:
            try:
                self.socket.sendall(enc)
            except Exception as e:
                print('ClientCom send_file - ', e)

    def recv_file(self, file_name, start_time, volume, proto):
        """
        receiving file from server
        :param file_name: file name
        :param start_time: start time
        :param volume: volume
        :param proto: protocol number
        :return: None
        """
        data = ""  # data to return
        try:
            # getting file bytes length
            length = int(self.socket.recv(8).decode())
        except Exception as e:
            print('clientCom recv_file - ', e)
        else:
            print(f'length - {length}')
            # receiving file
            file = bytearray()
            try:
                while len(file) < length:
                    slice = length - len(file)
                    if slice > 1024:
                        file.extend(self.socket.recv(1024))
                    else:
                        file.extend(self.socket.recv(slice))
                        break
            except Exception as e:
                print('clientCom recv_file - ', e)
            else:
                print(f'length2 - {len(file)}')
                file = self.encrypt.decrypt(file.decode())
                data = [proto, file_name, start_time, volume, file]
        # returning data
        return data

