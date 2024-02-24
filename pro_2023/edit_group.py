from server_com import ServerCom
from edit_group_com import EditGroupCom

import queue
from encrypt import Encrypt
from data_base import DB
import threading
from server_protocol import ServerProtocol
from music_strip import MusicStrip
import time
import os


class EditGroup:
    """class server for file editing with group"""
    def __init__(self, socket, username, group_name, server_q, encrypt, ip, file_port):
        """
        creating edit group object
        :param socket: first client socket
        :param ip: first client ip
        :param file_port: file port
        :param username: first client username
        :param group_name: group name
        """
        # running flag
        self.running = True
        # encrypt object
        self.encrypt = encrypt
        # group name
        self.group_name = group_name
        # queue for messages from clients
        self.msg_q = queue.Queue()
        # q to send messages to main server
        self.server_q = server_q
        # dictionary of msg queues for file servers {ip, queue}
        self.file_queues = {ip: queue.Queue()}
        # dictionary of strips {strip name : MusicStrip object}
        self.strips = {}
        # {strip_name:[list of changes]}
        self.changes = {}
        # dictionary of file servers {ip : file_server}
        self.file_servers = {}
        # creating edit group communication
        self.comm = EditGroupCom(self.msg_q, self.encrypt, socket, ip)
        # usernames = {ip, username}
        self.usernames = {ip: username}
        # dict {strip name : username}
        self.strip_edit = {}

        # setting strips
        self.set_strips()
        # creating file server for client
        self.file_servers[ip] = ServerCom(file_port, self.file_queues[ip], self.encrypt)
        print(f'init file_server - {self.file_servers}, {self.group_name}')
        # sending client port to open a file client
        self.comm.send([ip], ServerProtocol.file_server_port(str(file_port)))
        # handle msgs
        threading.Thread(target=self.handle_msgs).start()
        # handle files for first client
        threading.Thread(target=self.handle_files, args=(self.file_queues[ip],)).start()

    def handle_msgs(self):
        """
        handling msgs from server
        :return: None
        """
        while self.running:
            ip, msg = self.msg_q.get()

            if msg[0] == -1:    # close edit group
                # saving file
                self.save_file()
                self.server_q.put((ip, [-1, self.group_name]))
                self.running = False
            elif msg[0] == 0:
                # removing client
                self.remove_client_editing(ip)
                del self.usernames[ip]
                # closing client file server
                self.file_servers[ip].running = False
                del self.file_servers[ip]
                del self.file_queues[ip]
                # telling main server to remove client
                self.server_q.put((ip, [0]))
            elif msg[0] == 5:   # stop editing
                self.stop_edit(ip)
            elif msg[0] == 7:   # cut from beginning
                self.cut_beginning(ip, msg[1], msg[2])
            elif msg[0] == 8:   # cut from end
                self.cut_end(ip, msg[1], msg[2])
            elif msg[0] == 9:   # move strip
                self.move_strip(ip, msg[1], msg[2])
            elif msg[0] == 10:  # inc volume
                self.inc(ip, msg[1])
            elif msg[0] == 11:  # dec volume
                self.dec(ip, msg[1])
            elif msg[0] == 12:
                pass
            elif msg[0] == 13:  # start editing strip
                self.start_edit_strip(ip, msg[1])
            elif msg[0] == 14:  # delete strip
                self.delete_strip(ip, msg[1])
            elif msg[0] == 15:  # stop editing strip
                self.stop_edit_strip(ip, msg[1])
            elif msg[0] == 19:
                self.check_strip_exists(ip, msg[1])

    def handle_files(self, file_q):
        """
        handling file msgs from client
        :return: None
        """
        while self.running:
            ip, msg = file_q.get()

            if msg[0] == 16:    # add strip
                self.add_strip(msg[1], msg[2], msg[3], msg[4], ip)
            elif msg[0] == 20:  # strips request
                # sending to client details about file
                self.send_edit_file(ip)

    def add_editor(self, socket, username, ip, port):
        """
        adding socket to open clients
        :param socket: client socket
        :param ip: client ip
        :param port: file port
        :param username: username
        :return: None
        """
        print(f'{ip} - file_port - {port}')
        # adding client
        self.comm.open_clients[socket] = ip
        self.usernames[ip] = username
        self.file_queues[ip] = queue.Queue()
        # creating file server for client
        self.file_servers[ip] = ServerCom(port, self.file_queues[ip], self.encrypt)
        print(f'add file_server - {self.file_servers}, {self.group_name}')
        # sending client port to open a file client
        self.comm.send([ip], ServerProtocol.file_server_port(str(port)))

        # sending all strip editors
        for strip in self.strip_edit.keys():
            self.comm.send([ip], ServerProtocol.start_edit_strip(strip, self.strip_edit[strip]))

        # handle files for first client
        threading.Thread(target=self.handle_files, args=(self.file_queues[ip],)).start()

    def inc(self, ip, strip_name):
        """
        increasing volume and sending to client
        :param strip_name: strip name
        :param ip: client ip
        :return: None
        """
        # increasing volume
        self.strips[strip_name].volume += 10
        # sending editors to inc volume
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.inc_volume(strip_name))

    def dec(self, ip, strip_name):
        """
        decreasing volume and sending to client
        :param strip_name: strip name
        :param ip: client ip
        :return: None
        """
        # decreasing volume
        self.strips[strip_name].volume -= 10
        # sending editors to dec volume
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.dec_volume(strip_name))

    def add_strip(self, strip_name, start_time, volume, file, ip):
        """
        adds sends to users to add strips
        :param strip_name: strip name
        :param start_time: start time
        :param volume: volume
        :param file: file in bytes
        :param ip: ip to exclude
        :return: None
        """
        file_path = f'groups_files\\{self.group_name}\\{strip_name}.wav'  # file path
        # saving strip file
        with open(file_path, 'wb') as strip:
            strip.write(file)

        # adding strip to strips list
        self.strips[strip_name] = MusicStrip(None, strip_name, float(start_time)
                                                              , int(volume), f'groups_files\\{self.group_name}')
        print(f"strips - {self.strips.keys()}")

        # sending added strip to connected clients
        for i in self.comm.open_clients.values():
            if i != ip:
                # sending strip name
                self.file_servers[i].send([i], ServerProtocol.strip_name(strip_name))
                # sending starting point
                self.file_servers[i].send([i], ServerProtocol.send_start_time(start_time))
                # sending volume
                self.file_servers[i].send([i], ServerProtocol.send_volume(volume))
                # sending file
                self.file_servers[i].send_file(i, file_path)

    def send_edit_file(self, ip):
        """
        sending all strips to client if they exist
        :param ip: client ip
        :return: None
        """
        if len(self.strips) == 0:
            # sending client to open edit panel
            self.comm.send([ip], '29')
        else:
            # sending strips to client
            strips_num = str(len(self.strips)).zfill(2)    # amount of strips

            # sending amount of strips
            self.file_servers[ip].send([ip], ServerProtocol.strips_amount(strips_num))

            for strip in self.strips.keys():    # running on all strips
                strip_name = strip
                starting_point = str(self.strips[strip].starting_point)
                volume = str(self.strips[strip].volume)
                file_path = f'groups_files\\{self.group_name}\\{strip_name}.wav'   # file path

                # sending strip name
                self.file_servers[ip].send([ip], ServerProtocol.strip_name(strip_name))
                # sending starting point
                self.file_servers[ip].send([ip], ServerProtocol.send_start_time(starting_point))
                # sending volume
                self.file_servers[ip].send([ip], ServerProtocol.send_volume(volume))
                # sending file
                self.file_servers[ip].send_file(ip, file_path)

    def start_edit_strip(self, ip, strip_name):
        """
        sending to clients strip is being edit
        :param ip: ip
        :param strip_name: strip name
        :return: None
        """
        username = self.usernames[ip]
        if strip_name in self.strip_edit.keys():
            # sending to client strip is occupied
            self.comm.send([ip], ServerProtocol.strip_occupied(self.strip_edit[strip_name]))
        else:
            # sending to client that he can edit the strip
            self.comm.send([ip], '34')
            self.strip_edit[strip_name] = username
            # sending to all clients
            for i in self.comm.open_clients.values():
                if i != ip:
                    # sending message
                    self.comm.send([i], ServerProtocol.start_edit_strip(strip_name, username))

    def stop_edit_strip(self, ip, strip_name):
        """
        sending to clients strip is not being edit
        :param ip: ip
        :param strip_name: strip name
        :return: None
        """
        del self.strip_edit[strip_name]
        # sending to all clients
        for i in self.comm.open_clients.values():
            if i != ip:
                # sending message
                self.comm.send([i], ServerProtocol.stop_edit_strip(strip_name))

    def remove_client_editing(self, ip):
        """
        removing client from self.strip_edit
        :param ip: client ip
        :return: None
        """
        username = self.usernames[ip]
        if username in self.strip_edit.values():
            for strip in self.strip_edit.keys():
                if username == self.strip_edit[strip]:
                    self.stop_edit_strip(ip, strip)
                    break

    def cut_beginning(self, ip, strip_name, cut_time):
        """
        cutting from beginning
        :param ip: client ip
        :param strip_name: strip name
        :param cut_time: cut time
        :return: None
        """
        # cutting strip
        self.strips[strip_name].trim_start(float(cut_time))
        # saving file
        self.strips[strip_name].save_file()
        # sending to clients to cut their strip
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.shorten_start(strip_name, cut_time))

    def cut_end(self, ip, strip_name, cut_time):
        """
        cutting from end
        :param ip: client ip
        :param strip_name: strip name
        :param cut_time: cut time
        :return: None
        """
        # cutting strip
        self.strips[strip_name].trim_end(float(cut_time))
        # saving file
        self.strips[strip_name].save_file()
        # sending to clients to cut their strip
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.shorten_end(strip_name, cut_time))

    def move_strip(self, ip, strip_name, starting_point):
        """
        moving strip and telling other clients to move strip
         :param ip: client ip
        :param strip_name: strip name
        :param starting_point: new starting point
        :return: None
        """
        # changing starting point
        self.strips[strip_name].starting_point = float(starting_point)

        # telling other members to change starting point
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.move_strip(strip_name, starting_point))

    def delete_strip(self, ip, strip_name):
        """
        deleting strip
        :param ip: ip
        :param strip_name: strip name
        :return: None
        """
        # deleting strip file
        os.remove(f'groups_files\\{self.group_name}\\{strip_name}.wav')
        # deleting from dictionaries
        del self.strip_edit[strip_name]
        del self.strips[strip_name]

        # sending to clients to remove strip
        for i in self.comm.open_clients.values():
            if i != ip:
                self.comm.send([i], ServerProtocol.delete_strip(strip_name))

    def check_strip_exists(self, ip, strip_name):
        """
        checking if strip exists and telling client
        :param strip_name: strip name
        :param ip: client ip
        :return: None
        """
        if strip_name in self.strips.keys():
            self.comm.send([ip], '31')
        else:
            self.comm.send([ip], '30')

    def stop_edit(self, ip):
        """
        disconnecting client
        :param ip: client ip
        :return: None
        """
        socket = self.comm.find_socket_by_ip(ip)
        # removing client
        self.remove_client_editing(ip)
        del self.usernames[ip]
        # closing client file server
        self.file_servers[ip].running = False
        del self.file_servers[ip]
        del self.file_queues[ip]
        # removing socket
        del self.comm.open_clients[socket]
        # telling server to return client
        self.server_q.put((ip, [-2, socket]))

        if len(self.comm.open_clients.keys()) == 0:
            self.msg_q.put((ip, [-1]))
            self.comm.running = False

    def set_strips(self):
        """
        setting strips
        :return: None
        """
        db = DB()   # data base object
        strips = db.get_details(self.group_name.split(';')[0], self.group_name.split(';')[1])
        if strips is not None and strips != '':
            for strip in strips.split('|'):
                self.strips[strip.split(';')[0]] = MusicStrip(None, strip.split(';')[0], float(strip.split(';')[1])
                                                    , int(strip.split(';')[2]), f'groups_files\\{self.group_name}')

    def save_file(self):
        """
        saving edit file in data base
        :return: None
        """
        db = DB()  # data base object
        details = ''    # details to save
        counter = 0     # counter
        for strip in self.strips.keys():
            # writing details
            if counter > 0:
                details += '|'
                print(f'stating point - {self.strips[strip].starting_point}')
            details += f'{strip};{self.strips[strip].starting_point};{self.strips[strip].volume}'
            counter += 1
        # saving details in data base
        db.update_file(self.group_name.split(';')[0], self.group_name.split(';')[1], details)
        # deleting all files from undo folder
        path = f'groups_files\\{self.group_name}\\undo'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        # closing data base
        db.close_db()
