import socket
import threading
import select
from server_protocol import ServerProtocol


class EditGroupCom:
    """
    edit group server communication
    """

    def __init__(self, msg_q, encrypt, socket, ip):
        """
        initializing object parameters and calling the thread main loop
        :param ip: client ip
        :param msg_q: queue for messages
        :param encrypt: encrypt decrypt object
        """
        self.msg_q = msg_q
        self.encrypt = encrypt
        self.open_clients = {socket: ip}      # dictionary of open clients
        self.running = True

        # calling main_loop thread
        threading.Thread(target=self._main_loop).start()

    def _main_loop(self):
        """
        creating server socket starts to accept new clients
        putting their messages in msg_q and calling _diffie() for new clients
        :return: None
        """
        while self.running:
            if len(self.open_clients.keys()) > 0:
                rlist, wlist, xlist = select.select(list(self.open_clients.keys()), [], [], 0.1)
                for current_socket in rlist:

                    if current_socket in self.open_clients.keys():
                        try:
                            data_len = current_socket.recv(5).decode()  # getting data length
                            data = current_socket.recv(int(data_len))  # getting data
                            # decrypting data
                            data = self.encrypt.decrypt(data, self.open_clients[current_socket]).decode()
                        except Exception as e:
                            print("EditGroupCom - _main_loop" + str(e))
                            self._disconnect_client(current_socket)
                        else:
                            if data == "":
                                self._disconnect_client(current_socket)
                            else:
                                if current_socket in self.open_clients.keys():  # if socket open clients
                                    if type(data) == str:   # if not receive file
                                        data = ServerProtocol.unpack(data)
                                    self.msg_q.put((self.open_clients[current_socket], data))
            else:
                break

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

            try:
                enc = self.encrypt.encrypt(msg, self.open_clients[soc])
                # sending length of message
                soc.send(str(len(enc)).zfill(5).encode())
                # sending message
                soc.send(enc)
            except Exception as e:
                print('EditGroupCom send - ', e)
                self._disconnect_client(soc)

    def _disconnect_client(self, socket):
        """
        disconnects socket and removes socket from open_clients
        :param socket: socket to disconnect
        :return: None
        """
        # telling server to delete username
        self.msg_q.put((self.open_clients[socket], [0]))
        if len(self.open_clients.keys()) == 1:
            self.msg_q.put((self.open_clients[socket], [-1]))
            self.running = False
        # removing socket
        del self.open_clients[socket]
        socket.close()  # closing socket

    def find_socket_by_ip(self, ip):
        """
        returning socket from ip
        :param ip: ip
        :return: socket
        """
        socket = None
        for soc in self.open_clients.keys():
            if self.open_clients[soc] == ip:
                socket = soc
                break
        return socket