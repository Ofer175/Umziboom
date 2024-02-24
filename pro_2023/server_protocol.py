class ServerProtocol:
    """
    class to build messages based on server protocol
    """

    @staticmethod
    def usernames(usernames):
        """
        usernames message
        :param usernames: username

        :return: message based on protocol
        """
        message = '07'+','.join(usernames)
        return message

    @staticmethod
    def edit_files(edit_files):
        """
        edit files message
        :param edit_files: list of  edit files names
        :return: message based on protocol
        """
        message = '06'+'|'.join(edit_files)
        return message

    @staticmethod
    def added_file(file_name):
        """
        added file message
        :param file_name: file name
        :return: message based on protocol
        """
        message = '08' + file_name
        return message

    @staticmethod
    def added_user(username):
        """
        added user message
        :param username: username
        :return: message based on protocol
        """
        message = '09'+username
        return message

    @staticmethod
    def shorten_start(strip_name, time_to_take):
        """
        shorten start messsage
        :param strip_name: strip name
        :param time_to_take: time to take
        :return: message based on protocol
        """
        message = '10' + strip_name + '|' + str(time_to_take)
        return message

    @staticmethod
    def shorten_end(strip_name, time_to_take):
        """
        shorten end messsage
        :param strip_name: strip name
        :param time_to_take: time to take
        :return: message based on protocol
        """
        message = '11' + strip_name + '|' + str(time_to_take)
        return message

    @staticmethod
    def move_strip(strip_name, start_time):
        """
        move strip message
        :param strip_name: strip name
        :param start_time: start time
        :return: message based on protocol
        """
        message = '12' + strip_name + '|' + str(start_time)
        return message

    @staticmethod
    def inc_volume(strip_name):
        """
        increase volume message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '13' + strip_name
        return message

    @staticmethod
    def dec_volume(strip_name):
        """
        decrease volume message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '14' + strip_name
        return message

    @staticmethod
    def undo(strip_name):
        """
        undo message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '15' + strip_name
        return message

    @staticmethod
    def editing_members(usernames):
        """
        editing members message
        :param usernames: usernames
        :return: message based on protocol
        """
        message = '17' + str(usernames)[1:-1]
        return message

    @staticmethod
    def start_edit_strip(strip_name, username):
        """
        start edit strip message
        :param strip_name: strip name
        :param username:
        :return: message based on protocol
        """
        message = '18' + strip_name + "|" + username
        return message

    @staticmethod
    def stop_edit_strip(strip_name):
        """
        stop edit strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '19' + strip_name
        return message

    @staticmethod
    def delete_strip(strip_name):
        """
        delete strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '20' + strip_name
        return message

    @staticmethod
    def file_server_port(port):
        """
        file server port message
        :param port: server port
        :return: message based on protocol
        """
        message = '24' + port
        return message

    @staticmethod
    def strip_name(strip_name):
        """
        add strip message
        :param strip_name: strip name
        :return: message based on protocol
        """
        message = '25' + strip_name
        return message

    @staticmethod
    def send_start_time(starting_point):
        """
        strip starting point message
        :param starting_point: starting point
        :return: message based on protocol
        """
        message = '26' + starting_point
        return message

    @staticmethod
    def send_volume(volume):
        """
        strip volume message
        :param volume: volume
        :return: message based on protocol
        """
        message = '27' + volume
        return message

    @staticmethod
    def strips_amount(amount):
        """
        amount of strips
        :param volume: volume
        :return: message based on protocol
        """
        message = '28' + amount
        return message

    @staticmethod
    def strip_occupied(editor_name):
        """
        sending strip is occupied
        :param editor_name: editor name
        :return: message based on protocol
        """
        message = '33' + editor_name
        return message

    @staticmethod
    def unpack(msg):
        """
        unpacks messages from client
        :param msg: msg in protocol
        :return: list of opcode params
        """
        return_list = []    # list to return

        # number of protocol
        proto_num = int(msg[:2])

        # unpacking
        if '|' not in msg:
            return_list = [proto_num, msg[2:]]

        else:
            return_list = [proto_num] + msg[2:].split('|')

        return return_list


def main():
    pass


if __name__ == '__main__':
    main()















