import imp
import os
import sys
import json

action_list = []

current_path = os.path.dirname(os.path.abspath(__file__))

def load_all(config_name):
    config_name = os.path.join(current_path, config_name)

    config_file = open(config_name, 'r')
    config = json.load(config_file)
    config_file.close()
    
    print('Loading plugins . . .')
    py_files = filter(lambda x: os.path.isfile(os.path.join(current_path, 'plugins', x)) and x.lower().endswith('.py'), os.listdir(os.path.join(current_path, 'plugins')))
    for py_file in py_files:
        plugin = load(py_file)
        # TODO: dictionary lookup that returns None on failure?
        if plugin.__name__ in config:
            actions = plugin.get(config[plugin.__name__])
        else:
            actions = plugin.get(None)
        print('* {0} - ({1})'.format(plugin.__name__, len(actions)))
        action_list.extend(actions)
    print('Done')

def load(filename):
    full_path = os.path.join(current_path, 'plugins', filename)
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
    
