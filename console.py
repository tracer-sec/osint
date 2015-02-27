import plugins
import json
import sys
import data
import model

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()
    
plugins.load_all(config)

target = sys.argv[1]

start_node = model.Node('person', target)

d = data.Storage(target)
d.add_node(start_node)

while True:
    command = raw_input('> ')
    tokens = command.split(' ')
    if tokens[0].lower() == 'quit':
        break
        
    elif tokens[0].lower() == 'list':
        # show list of nodes
        if tokens[1].lower() == 'nodes':
            nodes = d.get_nodes()
            print('\n'.join(map(lambda x: str(x), nodes)))
        elif tokens[1].lower() == 'actions':
            actions = plugins.fetch_actions(tokens[2])
            print('\n'.join(map(lambda x: str(x), actions)))
                
    elif tokens[0].lower() == 'get':
        id = int(tokens[1])
        result = d.get_node(id)
        print(result)
        
    elif tokens[0].lower() == 'run':
        # run plugin
        action_name = tokens[1]
        action = plugins.fetch(action_name)
        target_id = int(tokens[2])
        target = d.get_node(target_id)
        result = action['func'](target)
        for n in result:
            d.add_node(n)
            connection = model.Connection(target.id, n.id, action_name, 'concrete', '')
            d.add_connection(connection)
        print(result)
        
    else:
        print('< Unknown command: ' + command)
    