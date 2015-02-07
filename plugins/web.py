import whois
import httplib
import urlparse
import utils
import model
import re

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
    domain = utils.get_domain(node.name)
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
        }
    ]
    