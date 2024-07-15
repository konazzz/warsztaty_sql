from psycopg2 import connect
USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"


class User:
    def __init__(self, username, hashed_password):
        self._id = -1
        self.username = username
        self._hashed_password = hashed_password

    @property
    def _id(self):
        return self._id
    
    @property
    def hashed_password(self):
        return self.hashed_password
    
    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True
    

class Message:
    def __init__(self, text):
        self._id = -1
        self.from_id = -1
        self.to_id = -1
        self.text = text
        self.creation_data = None

    @property
    def _id(self):
        return self._id
    

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO message(from_id, to_id, text, creation_date)
                            VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET from_id=%s, to_id=%s, text=%s
                           WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id, from_id, to_id, text, creation_date = row
            loaded_message = Message()
            loaded_message._id = id
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = text
            loaded_message.creation_date = creation_date
            messages.append(loaded_message)
        return messages
