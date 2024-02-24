from pydub import AudioSegment
import os


class MusicStrip:
    """
    class to make edits in music and create a strip object
    """

    def __init__(self, file, name, starting_point, volume, path):
        """
        creates a strip object
        :param file: file in bytes
        :param name: strip name
        :param path: path to save file
        :param starting_point: starting time
        :param volume: volume
        """
        self.name = name    # strip name
        self.path = path    # strip path

        if file:    # client
            # saving file
            with open(self.path+'\\'+name+'.wav', 'wb') as strip:
                strip.write(file)
        self.file = AudioSegment.from_wav(self.path+'\\'+name+'.wav')     # pydub file
        self.length = self.file.duration_seconds   # length of file in seconds
        self.muted = False  # if strip is muted
        self.volume = volume     # strip volume
        self.starting_point = starting_point    # starting point of strip

    def trim_start(self, time):
        """
        trimming from start
        :param time: time to trim
        :return: None
        """
        self.file = self.file[time:]    # trimming file
        self.length = self.file.duration_seconds    # updating time
        self.starting_point += time/1000     # updating starting point

    def trim_end(self, time):
        """
        trimming from end
        :param time: time to trim
        :return: None
        """
        self.file = self.file[:-time]  # trimming file
        self.length = self.file.duration_seconds  # updating time

    def set_strip(self, file, starting_point, volume):
        """
        setting strip with parameters
        :param file: music file in bytes
        :param starting_point: starting point
        :param volume: volume
        :return: None
        """
        # saving file
        with open(self.path+'\\' + self.name + '.wav', 'wb') as strip:
            strip.write(file)

        self.file = AudioSegment.from_wav('client_music\\' + self.name + '.wav')  # pydub file
        self.length = self.file.duration_seconds  # length of file in seconds
        self.volume = volume  # strip volume
        self.starting_point = starting_point  # starting point of strip

    def save_file(self):
        """
        saving strip with volume
        :return: None
        """
        self.file.export(self.path+'\\' + self.name + '.wav', format='wav')  # export strip audio file


if __name__ == '__main__':

    pass


