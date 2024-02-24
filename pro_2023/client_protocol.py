class ClientProtocol:
    """
    class to build messages based on client protocol
    """

    @staticmethod
    def log_in(username, password):
        """
        creates log in message
        :param username: username
        :param password: password
        :return: message based on protocol
        """
        message = '01'+password+'|'+username
        return message

    @staticmethod
    def sign_in(username, password):
        """
         ign in message
        :param username: username
        :param password: password
        :return: message based on protocol
        """
        message = '02' + password + '|' + username
        return message

    @staticmethod
    def create_file(file_name):
        """
        create file message
        :param file_name: file name
        :return: message based on protocol
        """
        message = '03' + file_name
        return message

    @staticmethod
    def start_edit_file(file_name):
        """
        start edit file message
        :param file_name: file name
        :return: message based on protocol
        """
        message = '04' + file_name
        return message

    @staticmethod
    def shorten_start(strip_name, time_to_take):
        """
        shorten start messsage
        :param strip_name: strip name
        :param time_to_take: time to take
        :return: message based on protocol
        """
        message = '07' + strip_name + '|' + str(time_to_take)
        return message

    @staticmethod
    def shorten_end(strip_name, time_to_take):
        """
        shorten end messsage
        :param strip_name: strip name
        :param time_to_take: time to take
        :return: message based on protocol
        """
        message = '08' + strip_name + '|' + str(time_to_take)
        return message

    @staticmethod
    def move_strip(strip_name, start_time):
        """
        move strip message
        :param strip_name: strip name
        :param start_time: start time
        :return: message based on protocol
        """
        message = '09' + strip_name + '|' + str(start_time)
        return message

    @staticmethod
    def inc_volume(strip_name):
        """
        increase volume message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '10' + strip_name

    @staticmethod
    def dec_volume(strip_name):
        """
        decrease volume message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '11' + strip_name

    @staticmethod
    def undo(strip_name):
        """
        undo message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '12' + strip_name

    @staticmethod
    def start_edit_strip(strip_name):
        """
        start edit strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '13' + strip_name

    @staticmethod
    def delete_strip(strip_name):
        """
        delete strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '14' + strip_name

    @staticmethod
    def stop_editing_strip(strip_name):
        """
        send stop editing strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '15' + strip_name

    @staticmethod
    def add_strip(strip_name):
        """
        send strip name message
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '16' + strip_name

    @staticmethod
    def send_start_time(start_time):
        """
        send start time
        :param start_time: start time
        :return: message based on protocol
        """
        return '17' + start_time

    @staticmethod
    def send_volume(volume):
        """
        send start time
        :param volume: volume
        :return: message based on protocol
        """
        return '18' + volume

    @staticmethod
    def strip_name_request(strip_name):
        """
        send strip name
        :param strip_name: strip name
        :return: message based on protocol
        """
        return '19' + strip_name

    @staticmethod
    def unpack(msg):
        """
        unpacks messages from server
        :param msg: msg in protocol
        :return: list of opcode params
        """
        return_list = []  # list to return

        # number of protocol
        proto_num = int(msg[:2])

        # unpack
        if '|' not in msg:
            return_list = [proto_num, msg[2:]]

        else:
            return_list = [proto_num] + msg[2:].split('|')

        return return_list



def main():
    pass


if __name__ == '__main__':
    main()






























