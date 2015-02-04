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
        c.execute('CREATE TABLE nodes (id INTEGER PRIMARY KEY, node_type TEXT, name TEXT, data TEXT)')
        c.execute('CREATE TABLE connections (parent_id INTEGER, child_id INTEGER, connection_type TEXT, data TEXT)')
        self.connection.commit()
        
    def __del__(self):
        self.connection.close()
        
    def add_node(self, node):
        params = (node.node_type, node.name, json.dumps(node.data))
        c = self.connection.cursor()
        c.execute('INSERT INTO nodes (node_type, name, data) VALUES (?, ?, ?)', params)
        node.id = c.lastrowid
        self.connection.commit()
        return node
        
    def add_connection(self, connection):
        params = (connection.parent_id, connection.child_id, connection.connection_type, json.dumps(connection.data))
        c = self.connection.cursor()
        c.execute('INSERT INTO connections (parent_id, child_id, connection_type, data) VALUES (?, ?, ?, ?)', params)
        self.connection.commit()
        return connection

