import sqlite3
import datetime
import json

class Storage(object):
    def __init__(self, name):
        d = datetime.datetime.utcnow().isoformat('-').replace(':', '')
        d = d[:d.find('.')]  # microseconds? Er. Thanks. I'll pass
        filename = 'osint_{0}_{1}.db'.format(name, d)
        open(filename, 'a').close()
        self.connection = sqlite3.connect(filename)
        c = self.connection.cursor()
        c.execute('CREATE TABLE profile (id INTEGER PRIMARY KEY, provider TEXT, query TEXT, profile_id TEXT, name TEXT, data TEXT)')
        c.execute('CREATE TABLE connection (parent_id INTEGER, child_id INTEGER, data TEXT)')
        self.connection.commit()
        
    def __del__(self):
        self.connection.close()
        
    def add_profile(self, provider, query, profile_id, name, data, parent, connection_type):
        params = (provider, query, profile_id, name, json.dumps(data))
        c = self.connection.cursor()
        c.execute('INSERT INTO profile (provider, query, profile_id, name, data) VALUES (?, ?, ?, ?, ?)', params)
        new_id = c.lastrowid
        
        if parent is not None:
            parent_key = parent.split('~')
            c.execute('SELECT id FROM profile WHERE provider = ? AND profile_id = ?', (parent_key[0], parent_key[2]))
            p = c.fetchone()     
            if p is not None:
                c.execute('INSERT INTO connection (parent_id, child_id, data) VALUES (?, ?, ?)', (p[0], new_id, connection_type))
        
        self.connection.commit()
        
    def add_connection(self, parent_id, child_id, data):
        params = (parent_id, child_id, data)
        c = self.connection.cursor()
        c.execute('INSERT INTO connection (parent_id, child_id, data) VALUES (?, ?, ?)', params)
        self.connection.commit()

