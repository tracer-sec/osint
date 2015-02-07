import sqlite3
import datetime
import json
import model

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
        c = self.connection.cursor()
        if node.id > 0:
            c.execute('UPDATE nodes SET data = ? WHERE id = ?', (json.dumps(node.data), node.id))
        else:
            # First we check to see if this exists already.
            existing_node = self.get_node(node_type = node.node_type, name = node.name)
            if existing_node == None:
                params = (node.node_type, node.name, json.dumps(node.data))
                c.execute('INSERT INTO nodes (node_type, name, data) VALUES (?, ?, ?)', params)
                node.id = c.lastrowid
            else:
                # It does, so just grab the id so we can create the connection
                node.id = existing_node.id
        self.connection.commit()
        return node
        
    def add_connection(self, connection):
        params = (connection.parent_id, connection.child_id, connection.connection_type, json.dumps(connection.data))
        c = self.connection.cursor()
        c.execute('INSERT INTO connections (parent_id, child_id, connection_type, data) VALUES (?, ?, ?, ?)', params)
        self.connection.commit()
        return connection

    def get_nodes(self):
        c = self.connection.cursor()
        c.execute('SELECT id, node_type, name, data FROM nodes')
        result = [model.Node(x[1], x[2], x[3], x[0]) for x in c.fetchall()]
        return result

    def get_node(self, id = None, node_type = None, name = None):
        c = self.connection.cursor()
        if id is not None:
            c.execute('SELECT id, node_type, name, data FROM nodes WHERE id = ?', (id,))
        if node_type is not None and name is not None:
            c.execute('SELECT id, node_type, name, data FROM nodes WHERE node_type = ? AND name = ?', (node_type, name))
        x = c.fetchone()
        if x is None:
            result = None
        else:
            result = model.Node(x[1], x[2], x[3], x[0])
        return result
        
        