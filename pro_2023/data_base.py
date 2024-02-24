import sqlite3


class DB:
    """
    class to manage data base
    """

    def __init__(self):
        """
        creating DB object
        """
        self.db_name = 'MusicEditDB.db'     # data base name
        self.users_table = 'users'          # users table name
        self.editors_table = 'editFiles'    # editors table name
        self.conn = None
        self.cursor = None

        # creating data bass and tables
        self._create_db()

    def _create_db(self):
        """
        creates data bass and tables if they don't exist
        :return: None
        """

        # connecting to data base
        self.conn = sqlite3.connect(self.db_name)
        
        # creating cursor
        self.cursor = self.conn.cursor()

        # creating users table if not exists
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.users_table} 
                (username text, password text)''')

        # creating editFiles table if not exists
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.editors_table} 
                        (file_name text, group_members text, strips text)''')

        self.conn.commit()

    def _username_exists(self, username):
        """
        checks if username exists
        :param username: username
        :return: if username exists
        """
        sql = f"SELECT * FROM {self.users_table} WHERE username = ?"
        self.cursor.execute(sql, (username,))

        return self.cursor.fetchone()

    def add_user(self, username, password):
        """
        adds user if he does'nt already exists
        :param username: username
        :param password: password
        :return: if username was added or not
        """
        status = False

        # if username doesn't exist
        if not self._username_exists(username):
            sql = f"INSERT INTO {self.users_table} VALUES (?,?)"
            self.cursor.execute(sql, (username, password,))     # adding username and password
            self.conn.commit()
            status = True

        return status

    def check_password(self, username, password):
        """
        checks if password is correct
        :param username: username
        :param password: password
        :return: if password is correct
        """
        sql = f"SELECT password FROM {self.users_table} WHERE username = ?"
        self.cursor.execute(sql, (username,))
        password_got = self.cursor.fetchone()
        return password_got and password_got[0] == password

    def _file_exists(self, file_name, group_members):
        """
        checks if file name already exists for the group
        :param file_name: file name
        :param group_members: group editors
        :return: if file already exists
        """

        group_members = group_members.split(',')
        ret = False
        sql = f"SELECT group_members FROM {self.editors_table} WHERE file_name = ?"
        self.cursor.execute(sql, (file_name,))

        # getting files of group
        editor_names = self.cursor.fetchall()
        print(editor_names)

        # running on file names
        for i in editor_names:
            if ret:
                break
            for name in group_members:
                if name not in i[0].split(','):
                    ret = False
                    break
                ret = True

        return ret

    def add_file(self, file_name, group_members):
        """
        adds file if it doesn't already exist
        :param file_name: file name
        :param group_members: group members
        :return: if file was added
        """
        status = False

        # checking if file already exists
        if not self._file_exists(file_name, group_members):
            sql = f"INSERT INTO {self.editors_table} VALUES (?,?,?)"
            self.cursor.execute(sql, (file_name, group_members, None,))  # adding file name and group members
            self.conn.commit()
            status = True

        return status

    def update_file(self, file_name, group_members, details):
        """
        updates strips content
        :param file_name: file name
        :param group_members: group members
        :param details: details to update
        :return: None
        """
        sql = f"UPDATE {self.editors_table} SET strips = ? WHERE file_name = ? AND group_members = ?"
        self.cursor.execute(sql, (details, file_name, group_members,))  # adding file name and group members
        self.conn.commit()

    def get_details(self, file_name, group_members):
        """
        gets details of file strips
        :param file_name: file name
        :param group_members: group members
        :return: details of file strips
        """
        sql = f"SELECT strips FROM {self.editors_table} WHERE file_name = ? AND group_members = ?"
        self.cursor.execute(sql, (file_name, group_members,))
        return self.cursor.fetchone()[0]

    def get_users(self, username):
        """
        gets all names of users
        :param username: username to exclude
        :return: names of all users
        """
        sql = f"SELECT username FROM {self.users_table} WHERE username != ?"
        self.cursor.execute(sql, (username, ))
        return [x[0] for x in self.cursor.fetchall()]

    def get_user_files(self, username):
        """
        gets all the files of user
        :param username: username
        :return: None
        """
        edit_files = []
        sql = f"SELECT file_name, group_members FROM {self.editors_table}"
        self.cursor.execute(sql)
        ans = self.cursor.fetchall()
        # finding edit files of username
        for i in ans:
            if username in i[1].split(','):
                edit_files.append(';'.join(i))
        return edit_files

    def close_db(self):
        """
        closes data base connection
        :return: None
        """
        self.conn.close()


if __name__ == '__main__':
    pass

