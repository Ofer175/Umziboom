from client_com import ClientCom
from encrypt import Encrypt
import queue
import threading
from gui import*
import wx
from pubsub import pub
from music_strip import MusicStrip
import os
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import time


class ClientLogic:
    """client logic"""
    def __init__(self):
        # queue for messages
        self.msg_q = queue.Queue()
        # queue for file messages
        self.file_q = queue.Queue()
        # encrypt object
        self.cp = Encrypt()
        # music strips {strip name: MusicStrip}
        self.strips = {}
        # client comm
        self.comm = ClientCom('127.0.0.1', 2000, self.msg_q, self.cp)
        # file comm
        self.file_comm = None
        # strips counter to receive strips
        self.strips_count = 0
        # simple audio play
        self.play = None
        # username of client
        self.username = ''

        # calling handle msgs
        threading.Thread(target=self.handle_msgs, daemon=True).start()

    def handle_msgs(self):
        """
        handling msgs from server
        :return: None
        """
        while True:
            msg = self.msg_q.get()
            if msg[0] == 1:  # username or password incorrect
                # telling pasword or username are incorrect
                wx.CallAfter(pub.sendMessage, "fail_login", msg='password or username are incorrect')
            elif msg[0] == 2:   # user already logged in
                wx.CallAfter(pub.sendMessage, "user_already_connected", msg='user is already connected')
            elif msg[0] == 3:   # sign in fail
                wx.CallAfter(pub.sendMessage, "fail_sign_in", msg='user already exists')
            elif msg[0] == 4:   # sign in successful
                wx.CallAfter(pub.sendMessage, "success_sign_in", event=None)
            elif msg[0] == 5:   # login successful
                wx.CallAfter(pub.sendMessage, "success_login", event=None)
            elif msg[0] == 6:   # receive edit file names
                wx.CallAfter(pub.sendMessage, "set_files", file_names=msg[1:])
            elif msg[0] == 7:   # receive user names
                self.username = msg[1].split(',')[0]
                # creating folder for client files
                if not os.path.isdir(f'client_music_{self.username}'):
                    os.mkdir(f'client_music_{self.username}')
                wx.CallAfter(pub.sendMessage, "set_users", users=msg[1].split(','))
            elif msg[0] == 8:   # add file
                wx.CallAfter(pub.sendMessage, "add_file", file_name=msg[1])
            elif msg[0] == 9:   # added user
                wx.CallAfter(pub.sendMessage, "add_user", username=msg[1])
            elif msg[0] == 10:  # cut_beginning
                self.cut_beginning(msg[1], msg[2])
                wx.CallAfter(pub.sendMessage, "cut_beginning", strip_name=msg[1], cut_time=float(msg[2]), flag=False)
            elif msg[0] == 11:  # cut end
                self.cut_end(msg[1], msg[2])
                wx.CallAfter(pub.sendMessage, "cut_end", strip_name=msg[1], cut_time=float(msg[2]), flag=False)
            elif msg[0] == 12:  # starting point
                self.move_strip(msg[1], msg[2])
                wx.CallAfter(pub.sendMessage, "move_strip", strip_name=msg[1], starting_point=float(msg[2]), flag=False)
            elif msg[0] == 13:  # inc volume
                self.inc(msg[1])
                wx.CallAfter(pub.sendMessage, "inc_volume", event=msg[1])
            elif msg[0] == 14:  # dec volume
                self.dec(msg[1])
                wx.CallAfter(pub.sendMessage, "dec_volume",  event=msg[1])
            elif msg[0] == 18:  # editor started editing
                wx.CallAfter(pub.sendMessage, "start_stop_edit", strip_name=msg[1], username=msg[2], edit=True)
            elif msg[0] == 19:  # editor stopped editing
                wx.CallAfter(pub.sendMessage, "start_stop_edit", strip_name=msg[1], username='', edit=False)
            elif msg[0] == 20:  # delete strip
                self.delete_strip(msg[1])
                wx.CallAfter(pub.sendMessage, "delete_strip", event=msg[1])
            elif msg[0] == 24:  # open file client
                port = int(msg[1])
                # opening a file client
                self.file_comm = ClientCom('192.168.4.71', port, self.file_q, self.cp)
                time.sleep(0.01)
                # sending message to server to get files
                self.file_comm.send('20')
                # sending file_comm to gui
                wx.CallAfter(pub.sendMessage, "file_comm", file_comm=self.file_comm)
                # starting handle files thread
                threading.Thread(target=self.handle_files, daemon=True).start()
            elif msg[0] == 29:  # you have no strips
                wx.CallAfter(pub.sendMessage, "open_edit", event=None)
            elif msg[0] == 30:  # strip name is ok
                wx.CallAfter(pub.sendMessage, "send_strip")
            elif msg[0] == 31:  # strip already exists
                wx.CallAfter(pub.sendMessage, "strip_exists", msg='strip name already exists in your edit file')
            elif msg[0] == 32:  # file already exists
                wx.CallAfter(pub.sendMessage, "file_exists", msg='file already exists')
            elif msg[0] == 33:  # strip occupied
                wx.CallAfter(pub.sendMessage, "strip_occupied", msg=f'{msg[1]} is already editing this strip')
            elif msg[0] == 34:  # edit strip
                wx.CallAfter(pub.sendMessage, "edit_strip")

    def handle_files(self):
        """
        handling msgs from file server
        :return: None
        """
        while True:
            msg = self.file_q.get()

            if msg[0] == 25:  # add strip
                print(f'\nfile strip name - {msg[1]}')
                self.add_strip(msg[1], float(msg[2]), int(msg[3]), msg[4])
                if self.strips_count > 1:
                    self.strips_count -= 1
                elif self.strips_count != 0:
                    # showing edit panel
                    wx.CallAfter(pub.sendMessage, "open_edit", event=None)
                    self.strips_count = 0
            elif msg[0] == 28:  # amount of strips to receive
                # show loading panel
                self.strips_count = int(msg[1])
                wx.CallAfter(pub.sendMessage, "loading", event=None)

    def add_strip(self, strip_name, starting_point, volume, file_path):
        """
        creates MusicStrip object
        :param file_path: file path
        :param strip_name: strip name
        :param starting_point: starting point
        :param volume: volume
        :return: None
        """
        flag = True
        if type(file_path) == str:
            # opening file
            with open(file_path, 'rb') as strip:
                file = strip.read()
        else:
            flag = False
            file = file_path
        self.strips[strip_name] = MusicStrip(file, strip_name, starting_point, volume, f'client_music_{self.username}')
        length = self.strips[strip_name].length

        # setting strip in gui
        wx.CallAfter(pub.sendMessage, "add_strip", strip_name=strip_name, starting_point=starting_point, volume=volume
                     , length=length, flag=flag)

    def layer_music(self, flag):
        """
        playing sound
        :param flag: if to skip muted files
        :return: song
        """
        # creating layered file
        song_time = 0
        song = None
        strips = []
        # getting list of unmuted strips
        for strip in self.strips.keys():
            if flag:
                strips.append(self.strips[strip])
            elif not self.strips[strip].muted:
                strips.append(self.strips[strip])
        if len(strips) > 0:
            # finding time of song
            for strip in strips:
                song_time = max((strip.length + strip.starting_point), song_time)
            song = AudioSegment.silent(duration=song_time*1000)  # song to play
            # layering files
            for strip in strips:
                song = song.overlay(strip.file + strip.volume, position=strip.starting_point*1000)
        return [song, song_time]

    def start_play(self):
        """
        getting layered file and playing it
        :return: None
        """
        song, song_time = self.layer_music(False)
        # playing file
        threading.Thread(target=self.play_music, args=(song, song_time,), daemon=True).start()

    def play_music(self, song, song_time):
        """
        playing music
        :param song: song to play
        :param song_time: song time
        :return: None
        """
        self.play = None
        if song:
            self.play = _play_with_simpleaudio(song)
            time.sleep(song_time)  # do some stuff inbetween
        self.stop_play_music()

    def stop_play_music(self):
        """
        stop playing music
        :return: None
        """
        if self.play:
            self.play.stop()
        wx.CallAfter(pub.sendMessage, "music_stopped", event=None)

    def mute_unmute(self, strip_name):
        """
        mutting or un mutting strip
        :param strip_name: strip name
        :return: None
        """

        if self.strips[strip_name].muted:
            self.strips[strip_name].muted = False
        else:
            self.strips[strip_name].muted = True

    def inc(self, strip_name):
        """
        increasing volume on strips
        :param strip_name: strip name
        :return: None
        """
        self.strips[strip_name].volume += 10

    def dec(self, strip_name):
        """
        decreasing volume on strips
        :param strip_name: strip name
        :return: None
        """
        self.strips[strip_name].volume -= 10

    def cut_beginning(self, strip_name, time):
        """
        cutting from beginning
        :param strip_name: strip_name
        :param time: time to cut
        :return: None
        """
        self.strips[strip_name].trim_start(float(time))

    def cut_end(self, strip_name, time):
        """
        cutting from end
        :param strip_name: strip_name
        :param time: time to cut
        :return: None
        """
        self.strips[strip_name].trim_end(float(time))

    def move_strip(self, strip_name, time):
        """
        moving strip
        :param strip_name: strip_name
        :param time: time to cut
        :return: None
        """
        if type(time) == str:
            time = float(time)
        self.strips[strip_name].starting_point = time

    def delete_strip(self, strip_name):
        """
        deleting strip
        :param strip_name: strip name
        :return: None
        """
        # deleting file
        strip_path = f'client_music_{self.username}\\{strip_name}.wav'
        if os.path.exists(path=strip_path) and os.path.isfile(path=strip_path):
            os.remove(path=strip_path)
        # deleting from dictionaries
        del self.strips[strip_name]

    def stop_edit(self):
        """
        stop editing shared file
        :return: None
        """
        # deleting all strips
        self.strips.clear()
        self.delete_files()

    def graphic_loop(self):
        """
        starting graphics
        :return: None
        """
        app = wx.App(False)
        frame = Program(self.comm)
        frame.Show()
        app.MainLoop()

    def save_file(self, file_path):
        """
        saving file in given path
        :param file_path: file path
        :return: None
        """
        file, song_time = self.layer_music(True)
        file.export(file_path+'.wav', format='wav')  # export strip audio file

    def delete_files(self):
        """
        delering all files from client directory
        :return: None
        """
        # deleting all files from client_music directory
        path = f'client_music_{self.username}'
        for f in os.listdir(path):
            if os.path.exists(path=os.path.join(path, f)) and os.path.isfile(path=os.path.join(path, f)):
                os.remove(os.path.join(path, f))


def main():
    logic = ClientLogic()   # logic object
    # pubsubs
    pub.subscribe(logic.add_strip, "add_strip_logic")
    pub.subscribe(logic.start_play, "play_music")
    pub.subscribe(logic.stop_play_music, "stop_play")
    pub.subscribe(logic.mute_unmute, "mute")
    pub.subscribe(logic.inc, "inc")
    pub.subscribe(logic.dec, "dec")
    pub.subscribe(logic.cut_beginning, "beginning")
    pub.subscribe(logic.cut_end, "end")
    pub.subscribe(logic.save_file, "save_file")
    pub.subscribe(logic.move_strip, "move")
    pub.subscribe(logic.delete_strip, "delete")
    pub.subscribe(logic.stop_edit, "back")

    # graphic loop
    logic.graphic_loop()

    # deleting all files from client_music directory
    path = f'client_music_{logic.username}'
    if os.path.isdir(path):
        logic.delete_files()
        os.rmdir(path)


if __name__ == '__main__':
    main()





