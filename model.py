# node_types: person, twitter, reddit, domain, website, email
import json

class Node(object):
    def __init__(self, node_type, name, data = {}, id = -1):
        self.node_type = node_type
        self.name = name
        self.id = id        # gets assigned when saved
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data
    
    def __repr__(self):
        return '<{0} {1} {2}>'.format(self.node_type, self.name, self.id)
        
    @property
    def data_json(self):
        return json.dumps(self.data, sort_keys=True, indent=3)

        
# creation_type: concrete, manual, speculative
    
class Connection(object):
    def __init__(self, parent_id, child_id, connection_type, creation_type, data):
        self.parent_id = parent_id
        self.child_id = child_id
        self.connection_type = connection_type
        self.creation_type = creation_type
        self.data = data
    
    def __repr__(self):
        return '<{0} {1}>'.format(self.parent_id, self.child_id)
        