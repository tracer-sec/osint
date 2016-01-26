import imp
import os
import sys
import json

action_list = []
client_list = {}

current_path = os.path.dirname(os.path.abspath(__file__))

def load_all(config_name):
    success = True
    print('Loading config . . .')
    try:
        config_name = os.path.join(current_path, config_name)

        config_file = open(config_name, 'r')
        config = json.load(config_file)
        config_file.close()

        print('Done')
    except Exception as ex:
        success = False
        print(ex)

    print('Loading clients . . .')
    py_files = filter(lambda x: os.path.isfile(os.path.join(current_path, 'clients', x)) and x.lower().endswith('.py'), os.listdir(os.path.join(current_path, 'clients')))
    for py_file in py_files:
        try:
            plugin = load(py_file, 'clients')
            # TODO: dictionary lookup that returns None on failure?
            if plugin.__name__ in config:
                client = plugin.get(config[plugin.__name__])
            else:
                client = plugin.get(None)
            client_list[plugin.__name__] = client
            print('* {0}'.format(plugin.__name__))
        except Exception as ex:
            success = False
            print(ex)
    print('Done')

    print('Loading plugins . . .')
    py_files = filter(lambda x: os.path.isfile(os.path.join(current_path, 'plugins', x)) and x.lower().endswith('.py'), os.listdir(os.path.join(current_path, 'plugins')))
    for py_file in py_files:
        try:
            plugin = load(py_file, 'plugins')
            # TODO: dictionary lookup that returns None on failure?
            if plugin.__name__ in config:
                actions = plugin.get(config[plugin.__name__])
            else:
                actions = plugin.get(None)
            print('* {0} - ({1})'.format(plugin.__name__, len(actions)))
            action_list.extend(actions)
        except Exception as ex:
            success = False
            print(ex)
    print('Done')
    
    if not success:
        print("*** some failures while loading!")

def load(filename, subdir):
    full_path = os.path.join(current_path, subdir, filename)
    module_name = filename[:-3]
    return imp.load_source(module_name, full_path)

def fetch_actions(node_type):
    node_actions = filter(lambda x: node_type in x['acts_on'] or '*' in x['acts_on']
, action_list)
    return sorted(node_actions, key=lambda x: x['func'].__name__)

def fetch(action_name):
    # find?
    result = filter(lambda x: x['func'].__name__ == action_name, action_list)
    return None if len(result) == 0 else result[0]

import traceback

def run(node, action_name):
    result = []
    try:
        action = fetch(action_name)
        if action is not None:
            result = action['func'](node)
            for newNode in result:
                # If we're missing node data, fill it if, assuming
                # we have an appropriate client
                if newNode.data is None:
                    if newNode.node_type in client_list:
                        client_list[newNode.node_type].get_data(newNode)
                    else:
                        newNode.data = {}
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    return result
    
