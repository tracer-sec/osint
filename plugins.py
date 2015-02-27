import imp
import os
import sys

action_list = []

def load_all(config):
    print('Loading plugins . . .')
    py_files = filter(lambda x: os.path.isfile(os.path.join('plugins', x)) and x.lower().endswith('.py'), os.listdir('plugins'))
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
    full_path = os.path.join('plugins', filename)
    module_name = filename[:-3]
    return imp.load_source(module_name, full_path)

def fetch_actions(node_type):
    return filter(lambda x: node_type in x['acts_on'], action_list)

def fetch(action_name):
    # find?
    result = filter(lambda x: x['func'].__name__ == action_name, action_list)
    return None if len(result) == 0 else result[0]
    