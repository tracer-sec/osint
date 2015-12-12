import whois
import httplib
import urlparse
import model
import re
import webclient

BORING_HEADERS = [
    'etag',
    'content-length',
    'content-type',
    'date',
    'expires',
    'pragma',
    'vary',
    'cache-control'
]

SOCIAL_MEDIA_URLS = {
    'twitter': 'https?://twitter.com/([A-Za-z0-9_-]+)',
    'github': 'https?://github.com/([A-Za-z0-9_-]+)'
}

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
    try:
        whois_info = whois.lookup(node.name, True)
        node.data['whois'] = whois_info
    except Exception as e:
        print(e)
    return []
    

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


def get_social_links(node):
    client = webclient.WebClient(node.name)
    links = client.get_links()
    result = []
    for link in links:
        for r in SOCIAL_MEDIA_URLS.keys():
            m = SOCIAL_MEDIA_URLS[r].match(link)
            if m is not None:
                result.append(model.Node(r, m.group(1), None))
    return result

for r in SOCIAL_MEDIA_URLS.keys():
    SOCIAL_MEDIA_URLS[r] = re.compile(SOCIAL_MEDIA_URLS[r])


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
    
