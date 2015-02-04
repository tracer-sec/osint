# node_types: person, twitter, reddit, domain, website, email

class Node(object):
    def __init__(self, node_type, name, data):
        self.node_type = node_type
        self.name = name
        self.data = data
        self.id = -1        # gets assigned when saved
    
    def __repr__(self):
        return '<{0} {1} {2}>'.format(self.node_type, self.name, self.id)

        
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
        