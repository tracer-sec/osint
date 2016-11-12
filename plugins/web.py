import httplib
import urlparse
import model
import re

client = None

def get_domain(node):
    if '@' in node.name:
        # it's an email address
        domain = node.name[node.name.index('@') + 1:]
    else:
        result = urlparse.urlparse(node.name)
        domain = result.netloc
    n = model.Node('domain', domain, None)
    return [n]

def get_http_server_headers(node):
    client.get_http_server_headers(node)
    return []

def get_social_links(node):
    return client.get_social_links(node)

def get(config, c):
    global client
    client = c

    return [
        {
            'func': get_domain,
            'name': 'Domain',
            'acts_on': ['website', 'email']
        },
        {
            'func': get_http_server_headers,
            'name': 'Get HTTP server headers',
            'acts_on': ['website']
        },
        {
            'func': get_social_links,
            'name': 'Get social links from homepage',
            'acts_on': ['website']
        }
    ]
    
