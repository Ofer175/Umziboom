from server_com import ServerCom
import queue
from encrypt import Encrypt
from data_base import DB
import threading
from server_protocol import ServerProtocol
from edit_group import EditGroup
import os
import time


class ServerLogic:
    """server logic"""
    def __init__(self):
        # encrypt object
        self.cp = Encrypt()
        # queue for messages
        self.msg_q = queue.Queue()
        # communication object
        self.comm = ServerCom(2000, self.msg_q, self.cp)
        # editing groups = {file name : EditGroup}
        self.editing_groups = {}
        # usernames = {ip, username}
        self.usernames = {}
        # file ports {ip, file port}
        self.file_ports = {}
        # list of remaining ports
        self.remaining_ports = []
        # current file port
        self.current_file_port = 2000
        # handle msgs
        threading.Thread(target=self.handle_msgs).start()

    def handle_msgs(self):
        """
        handling msgs from server
        :return: None
        """

        while True:
            ip, msg = self.msg_q.get()

            if msg[0] == -1:    # close edit group
                del self.editing_groups[msg[1]]
            elif msg[0] == -2:  # stop editing shared file
                self.stop_edit(ip, msg[1])
            if msg[0] == 0:    # user disconnected
                print('file ports - ', self.file_ports)
                if ip in self.file_ports.keys():
                    self.remaining_ports.append(self.file_ports[ip])
                    del self.file_ports[ip]
                del self.cp.encrypt_keys[ip]
                if ip in self.usernames.keys():
                    del self.usernames[ip]
            elif msg[0] == 1:    # log in
                self.log_in(ip, msg[1], msg[2])
            elif msg[0] == 2:   # sign up
                self.sign_in(ip, msg[1], msg[2])
            elif msg[0] == 3:   # create edit file request
                self.create_edit_file(ip, msg[1])
            elif msg[0] == 4:   # edit file
                self.edit_file(ip, msg[1])
            elif msg[0] == 5:
                pass
            elif msg[0] == 6:
                pass
            elif msg[0] == 7:
                pass
            elif msg[0] == 8:
                pass
            elif msg[0] == 9:
                pass
            elif msg[0] == 10:
                pass
            elif msg[0] == 11:
                pass
            elif msg[0] == 12:
                pass
            elif msg[0] == 13:
                pass
            elif msg[0] == 14:
                pass
            elif msg[0] == 15:
                pass
            elif msg[0] == 16:
                pass
            elif msg[0] == 17:
                pass

    def log_in(self, ip, password, username):
        """
        checks if password and username are correct
        :param ip: client ip
        :param password: client password
        :param username: client username
        :return: None
        """
        db = DB()   # data base object

        # checking if user is already logged in
        if username not in self.usernames.values():
            password = str(Encrypt.hash(password))

            # checking if password is correct
            if db.check_password(username, password):
                # sending correct
                self.comm.send([ip], '05')
                # adding username to logged users
                self.usernames[ip] = username

                # sending the names of users to client
                usernames = [username] + db.get_users(username)
                if len(usernames) > 0:
                    self.comm.send([ip], ServerProtocol.usernames(usernames))

                # sending edit files
                edit_files = db.get_user_files(username)
                if len(edit_files) > 0:
                    self.comm.send([ip], ServerProtocol.edit_files(edit_files))

            else:
                # sending password or username are incorrect
                self.comm.send([ip], '01')
        else:
            # sending to client that the user is already logged in
            self.comm.send([ip], '02')
        # closing data base
        db.close_db()

    def sign_in(self, ip, password, username):
        """
        adding client if not exists
        :param ip: ip
        :param password: client password
        :param username: client username
        :return: None
        """
        db = DB()  # data base object
        password = str(Encrypt.hash(password))
        added = db.add_user(username, password)
        if added:
            # adding username to logged users
            self.usernames[ip] = username

            # sending user was added
            self.comm.send([ip], '04')

            # sending the names of users to client
            usernames = [username] + db.get_users(username)
            if len(usernames) > 0:
                self.comm.send([ip], ServerProtocol.usernames(usernames))

            # sending edit files
            edit_files = db.get_user_files(username)
            if len(edit_files) > 0:
                self.comm.send([ip], ServerProtocol.edit_files(edit_files))

            # sending to all connected clients the new added user
            self.send_add_user(username, ip)

        else:
            # sending user already exists
            self.comm.send([ip], '03')
        # closing data base
        db.close_db()

    def edit_file(self, ip, file_name):
        """
        sends to client details about edit file
        :param ip: client ip
        :param file_name: file name
        :return: None
        """
        soc = self.comm.find_socket_by_ip(ip)   # getting socket
        # removing client from open clients
        del self.comm.open_clients[soc]
        # getting port
        if len(self.remaining_ports) > 0:
            port = self.remaining_ports[0]
            self.remaining_ports.remove(port)
        else:
            self.current_file_port += 1
            port = self.current_file_port
        self.file_ports[ip] = port

        # checking if there's already an EditGroup object
        if file_name in self.editing_groups.keys():
            # adding client to edit group
            self.editing_groups[file_name].add_editor(soc, self.usernames[ip], ip, port)
        else:
            # creating an edit group object
            self.editing_groups[file_name] = EditGroup(soc, self.usernames[ip]
                                                       , file_name, self.msg_q, self.cp, ip, port)

    def create_edit_file(self, ip, file_name):
        """
        sending a message to client if file already exists and adding file if it does'nt exist
        :param ip: client ip
        :param file_name: file name
        :return: None
        """
        db = DB()  # data base object
        file = file_name.split(';')[0]
        group_members = file_name.split(';')[1]

        # trying to add file to data base
        if db.add_file(file, group_members):
            # creating folder for edit file
            path = os.path.join('groups_files', file_name)
            os.mkdir(path)
            # creating folder for edit file undo
            path = os.path.join('groups_files', f'{file_name}\\undo')
            os.mkdir(path)
            # sending added file
            self.send_add_file(file_name, ip)
            self.edit_file(ip, file_name)
        else:
            # sending to client that file already exists
            self.comm.send([ip], '32')

    def send_add_user(self, username, ip):
        """
        sending to all connected clients the new added user
        :param username: username
        :param ip: client ip
        :return: None
        """
        if len(self.comm.open_clients) > 1:
            # sending to all connected users to add new user
            ips = list(self.comm.open_clients.values())
            ips.remove(ip)  # removing client ip
            self.comm.send(ips, ServerProtocol.added_user(username))

    def send_add_file(self, file_name, ip):
        """
        sending to all connected users the new added file
        :param file_name: file name
        :param ip: client ip
        :return: None
        """
        if len(self.comm.open_clients) > 1:
            ips = list(self.comm.open_clients.values())
            ips.remove(ip)  # removing client ip
            group_members = file_name.split(';')[1].split(",")
            send_ips = []
            for i in ips:   # finding which ips to send to
                if self.usernames[i] in group_members:
                    send_ips.append(i)
            if len(send_ips) > 0:
                # sending to clients file to add
                self.comm.send(send_ips, ServerProtocol.added_file(file_name))

    def stop_edit(self, ip, socket):
        """
        client stops edit
        :param ip: ip
        :param socket: client socket
        :return: None
        """
        # adding client to open clients
        self.comm.open_clients[socket] = ip
        # adding client port
        self.remaining_ports.append(self.file_ports[ip])
        del self.file_ports[ip]


def main():
    """ main server"""

    logic = ServerLogic()   # logic object


if __name__ == '__main__':
    main()








