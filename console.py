import plugins
import sys
import data
import model

plugins.load_all('config.json')

target = sys.argv[1]

start_node = model.Node('person', target)

d = data.Storage(target)
d.add_node(start_node)

def handle(tokens):        
    if tokens[0].lower() == 'list':
        # show list of nodes
        if len(tokens) > 1:
            if tokens[1].lower() == 'nodes':
                nodes = d.get_nodes()
                print('\n'.join(map(lambda x: str(x), nodes)))
            elif tokens[1].lower() == 'actions':
                if len(tokens) > 2:
                    actions = plugins.fetch_actions(tokens[2])
                    print('\n'.join(map(lambda x: str(x), actions)))
                else:
                    print('USAGE: list actions NODE_TYPE')
        else:
            print('USAGE: list (nodes | actions NODE_TYPE)')
                
    elif tokens[0].lower() == 'get':
        if len(tokens) > 1:
            id = int(tokens[1])
            result = d.get_node(id)
            print(result)
            print(result.data_json)
        else:
            print('USAGE: get NODE_ID')
        
    elif tokens[0].lower() == 'run':
        # run plugin
        if len(tokens) > 2:
            action_name = tokens[1]
            action = plugins.fetch(action_name)
            target_id = int(tokens[2])
            target = d.get_node(target_id)
            result = action['func'](target)
            for n in result:
                d.add_node(n)
                connection = model.Connection(target.id, n.id, action_name, 'concrete', '')
                d.add_connection(connection)
            d.add_node(target)
            print(result)
        else:
            print('USAGE: run ACTION NODE_ID')
        
    else:
        print('< Unknown command: ' + command)

while True:
    command = raw_input('> ')
    tokens = command.split(' ')
    if tokens[0].lower() == 'quit':
        break
    else:
        try:
            handle(tokens)
        except Exception as e:
            print(e)
    
