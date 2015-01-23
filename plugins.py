import imp
import os
import sys

plugin_list = dict()

def load_all(config):
    print('Loading plugins . . .')
    py_files = filter(lambda x: os.path.isfile(os.path.join('plugins', x)) and x.lower().endswith('.py'), os.listdir('plugins'))
    for py_file in py_files:
        plugin = load(py_file)
        # TODO: dictionary lookup that returns None on failure?
        if plugin.__name__ in config:
            client = plugin.get(config[plugin.__name__])
        else:
            client = plugin.get(None)
        print('* ' + plugin.__name__)
        plugin_list[plugin.__name__] = client
    print('Done')

def load(filename):
    full_path = os.path.join('plugins', filename)
    module_name = filename[:-3]
    return imp.load_source(module_name, full_path)

def fetch(name):
    return plugin_list[name]
    