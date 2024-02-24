import socket
import threading
import select
import random
from server_protocol import ServerProtocol


class ServerCom:
    """
    server communication
    """

    def __init__(self, port, msg_q, encrypt):
        """
        initializing object parameters and calling the thread main loop
        :param port: communication port
        :param msg_q: queue for messages
         :param encrypt: encrypt decrypt object
        """
        self.running = True
        self.my_socket = None
        self.port = port
        self.msg_q = msg_q
        self.encrypt = encrypt
        self.open_clients = {}      # dictionary of open clients {socket] ->ip

        # calling main_loop thread
        threading.Thread(target=self._main_loop).start()

    def _main_loop(self):
        """
        creating server socket starts to accept new clients
        putting their messages in msg_q and calling _diffie() for new clients
        :return: None
        """
        self.my_socket = socket.socket()
        self.my_socket.bind(('0.0.0.0', self.port))
        self.my_socket.listen(5)

        while self.running:
            rlist, wlist, xlist = select.select([self.my_socket] + list(self.open_clients.keys()), [], [], 0.1)
            for current_socket in rlist:
                if current_socket is self.my_socket:
                    client, addr = self.my_socket.accept()
                    print(f"{addr[0]} - connected")
                    if addr[0] in self.open_clients.values():   # checking if ip is already connected to prevent dos
                        self._disconnect_client(client)
                    elif self.port == 2000:   # checking if to exchange keys
                        # calling _diffie() thread to exchange key with client
                        threading.Thread(target=self._diffie, args=(client, addr,)).start()
                    else:
                        self.open_clients[client] = addr[0]  # adding client to open clients
                        print(f'main port - {self.port}, open - {self.open_clients}')
                else:
                    try:
                        data_len = current_socket.recv(5).decode()  # getting data length
                        data = current_socket.recv(int(data_len))  # getting data
                        # decrypting data
                        data = self.encrypt.decrypt(data, self.open_clients[current_socket]).decode()
                        if data[:2] == '16':    # if receive file
                            proto = int(data[:2])    # message protocol
                            file_name = data[2:]    # file name

                            # receiving starting point
                            data_len = current_socket.recv(5).decode()
                            start_time = current_socket.recv(int(data_len))
                            # decrypting data
                            start_time = self.encrypt.decrypt(start_time, self.open_clients[current_socket]).decode()
                            start_time = start_time[2:]  # removing protocol

                            # receiving volume
                            data_len = current_socket.recv(5).decode()
                            volume = current_socket.recv(int(data_len))
                            # decrypting data
                            volume = self.encrypt.decrypt(volume, self.open_clients[current_socket]).decode()
                            volume = volume[2:]  # removing protocol

                            # receiving file
                            data = self.recv_file(file_name, start_time, volume, current_socket, proto)
                    except Exception as e:
                        print("ServerCom - _main_loop. server_com.py:84 " + str(e))
                        self._disconnect_client(current_socket)
                    else:
                        if data == '':
                            self._disconnect_client(current_socket)
                        else:
                            if type(data) == str:   # if not receive file
                                data = ServerProtocol.unpack(data)
                            self.msg_q.put((self.open_clients[current_socket], data))

    def _diffie(self, client, addr):
        """
        exchanging key with client using Diffie Hellman protocol
        :param client: client socket
        :param addr: ip address of client
        :return: the encryption key
        """
        p = 5195977
        g = 35125

        private_a = random.randint(1, 9999)  # generating random private number
        A = (g ** private_a) % p  # number to exchange with client

        # sending A and receiving B
        try:
            # sending A
            message = str(A)
            client.send((str(len(message))+message).encode())

            # receiving B
            length = client.recv(1).decode()    # getting message length
            B = int(client.recv(int(length)).decode())

        except Exception as e:
            print('ServerCom _diffie - ', e)
            client.close()

        else:
            # calculating key
            key = (B ** private_a) % p

            print(f'{addr[0]}, key-{key}')
            self.open_clients[client] = addr[0]     # adding client to open clients
            self.encrypt.add_key(str(key), addr[0])  # adding key to encryption object

    def send(self, ips, msg):
        """
        sends msg to list of sockets
        :param ips: list of ips
        :param msg: message to send
        :return: None
        """

        # sending message to all clients
        for ip in ips:
            soc = self.find_socket_by_ip(ip)
            if soc in self.open_clients.keys():
                o = self.open_clients[soc]
                enc = self.encrypt.encrypt(msg, o)
                try:
                    # sending length of message
                    soc.send(str(len(enc)).zfill(5).encode())
                    # sending message
                    soc.send(enc)
                except Exception as e:
                    print(f'serverCom send -  ', e)
                    self._disconnect_client(soc)

    def _disconnect_client(self, socket):
        """
        disconnects socket and removes socket from open_clients
        :param socket: socket to disconnect
        :return: None
        """
        if socket in self.open_clients.keys():
            print(f'disconnect socket - {socket}')
            # telling server to delete username
            self.msg_q.put((self.open_clients[socket], [0]))
            # removing socket
            del self.open_clients[socket]
            socket.close()  # closing socket

    def find_socket_by_ip(self, ip):
        """
        returning socket from ip
        :param ip: ip
        :return: socket
        """
        print(f'find open - {self.open_clients}, port - {self.port}')
        socket = None
        for soc in self.open_clients.keys():
            if self.open_clients[soc] == ip:
                socket = soc
                break
        return socket

    def send_file(self, ip, file_path):
        """
        sending file to client
        :param ip: ip to send to
        :param file_path: file path
        :return: None
        """
        socket = self.find_socket_by_ip(ip)     # socket of client
        print(f'send_file ip - {ip}, soc - {socket}, open - {self.open_clients}, port - {self.port}, ip - {ip}')
        # getting file
        with open(file_path, 'rb') as strip:
            file = strip.read()
        enc = self.encrypt.encrypt(file, self.open_clients[socket])

        length = len(enc)
        print(f'length - {length}')
        try:
            socket.send(str(len(enc)).zfill(8).encode())  # sending file length
        except Exception as e:
            self._disconnect_client(socket)
            print('ServerCom send_file - ', e)
        else:
            try:
                socket.sendall(enc)
            except Exception as e:
                self._disconnect_client(socket)
                print('ServerCom send_file - ', e)

    def recv_file(self, file_name, start_time, volume, socket, proto):
        """
        receiving music file from client
        :param file_name: file name
        :param proto: protocol
        :param socket: client socket
        :param start_time: start time
        :param volume: volume
        :return: None
        """
        data = ""   # data to return
        try:
            # getting file bytes length
            length = int(socket.recv(8).decode())
        except Exception as e:
            self._disconnect_client(socket)
            print('serverCom recv_file - ', e)
        else:
            print(f'length - {length}')
            # receiving file
            file = bytearray()
            try:
                while len(file) < length:
                    slice = length - len(file)
                    if slice > 1024:
                        file.extend(socket.recv(1024))
                    else:
                        file.extend(socket.recv(slice))
                        break
            except Exception as e:
                self._disconnect_client(socket)
                print('serverCom recv_file - ', e)
            else:
                print(f'length2 - {len(file)}')
                file = self.encrypt.decrypt(file.decode(), self.open_clients[socket])
                data = [proto, file_name, start_time, volume, file]
        # returning data
        return data

