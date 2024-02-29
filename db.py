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

    def get_class_spells(self, selected_class):
        data = self.select(f"SELECT * FROM spell_info WHERE Classes LIKE '%{selected_class}%'")
        return data
    
    def get_spell(self, Name):
        data = self.select('SELECT * FROM spell_info WHERE spell_info.Name = ?', [Name])
        return data
    
    def get_user_loadouts(self, user_id):
        data = self.select('SELECT distinct * FROM loadouts WHERE loadouts.user_id = ?', [user_id])
        return data
    
    def insert_spell_for_loadout(self, user_id, loadout_name, loadout_class, description, spell_name):
        self.execute('INSERT INTO loadouts(user_id, loadout_name, class, description, spell_name) VALUES (?, ?, ?, ?, ?)',
                     [user_id, loadout_name, loadout_class, description, spell_name])
        
    def get_loadout_spell_names(self, loadout_name):
        data = self.select('SELECT loadouts.spell_name FROM loadouts WHERE loadouts.loadout_name = ?', [loadout_name])
        return data

    def close(self):
        self.conn.close()