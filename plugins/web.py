import whois
import httplib
import urlparse
import model
import re

BORING_HEADERS = [
    'etag',
    'set-cookie',
    'content-length',
    'content-type',
    'date',
    'expires',
    'pragma',
    'vary',
    'cache-control'
]

def get_site_info(node):
    '''
    u = urlparse.urlparse(node.name)
    if u.scheme == 'http':
        connection = httplib.HTTPConnection(u.netloc)
    elif u.scheme == 'https':
        connection = httplib.HTTPSConnection(u.netloc)

    # Server header, meta-tags, etc.

    connection.close()
    '''
    return []

def get_domain(node):
    if '@' in node.name:
        # it's an email address
        domain = node.name[node.name.index('@') + 1:]
    else:
        result = urlparse.urlparse(node.name)
        domain = result.netloc
    n = model.Node('domain', domain, {})
    return [n]

def get_whois(node):
    whois_info = whois.lookup(node.name, True)
    node.data['whois'] = whois_info
    return []
    
def extract_administrative_emails(node):
    email_nodes = []
    if 'whois' in node.data:
        whois_info = node.data['whois']
        email_addresses = re.findall('[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+', whois_info)
        for email_address in email_addresses:
            email_nodes.append(model.Node('email', email_address, {}))
    return email_nodes
    

def get_http_server_headers(node):
    # HEAD request to server
    # Grab headers from response
    u = urlparse.urlparse(node.name)
    if u.scheme == 'http':
        connection = httplib.HTTPConnection(u.netloc)
    elif u.scheme == 'https':
        connection = httplib.HTTPSConnection(u.netloc)
        
    connection.request('HEAD', '/')
    response = connection.getresponse()
    headers = response.getheaders()
    connection.close()

    # Filter out dull headers and add to the original node
    node.data['headers'] = filter(lambda x: x[0] not in BORING_HEADERS, headers)
    return []

    
def get(config):
    return [
        {
            'func': get_domain,
            'name': 'Domain',
            'acts_on': ['website', 'email']
        },
        {
            'func': get_whois,
            'name': 'Whois',
            'acts_on': ['domain']
        },
        {
            'func': extract_administrative_emails,
            'name': 'Administrative contact',
            'acts_on': ['domain']
        },
        {
            'func': get_http_server_headers,
            'name': 'Get HTTP server headers',
            'acts_on': ['website']
        }
    ]
    
