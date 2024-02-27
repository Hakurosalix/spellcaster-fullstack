import sqlite3


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def create_user(self, username, encrypted_password):
        self.execute('INSERT INTO users (username, encrypted_password) VALUES (?, ?)',
                     [username, encrypted_password])

    def get_user(self, username):
        data = self.select(
            'SELECT * FROM users WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'id': d[0],
                'username': d[1],
                'encrypted_password': d[2],
            }
        else:
            return None

    def close(self):
        self.conn.close()