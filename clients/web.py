import model
import httplib
import urlparse
from lxml import html
from lxml import etree
import re
import sys

SOCIAL_MEDIA_URLS = {
    'twitter': '^https?://twitter.com/([A-Za-z0-9_-]+)',
    'github': '^https?://github.com/([A-Za-z0-9_-]+)',   
    'facebook': '^https?://www.facebook.com/([A-Za-z0-9_-]+)',
    'instagram': '^https?://instagram.com/([A-Za-z0-9_-]+)', 
    'plus': '^https?://plus.google.com/([0-9]+)',
    'youtube': '^https?://www.youtube.com/user/([A-Za-z0-9_-]+)'
}

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

class WebClient(object):
    def __init__(self):
        self.social_regex = {}
        for r in SOCIAL_MEDIA_URLS.keys():
            self.social_regex[r] = re.compile(SOCIAL_MEDIA_URLS[r])

    def get_node(self, target):
        return model.Node('website', node, {})

    def get_data(self, node):
        pass

    def get_social_links(self, node):
        links = self._get_links(node.name)
        result = []
        for link in links:
            for r in self.social_regex.keys():
                m = self.social_regex[r].match(link)
                if m is not None:
                    result.append(model.Node(r, m.group(1), None))
        return result
    
    def get_http_server_headers(self, node):
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

    def _get_html(self, url):
        for i in range(5):
            u = urlparse.urlparse(url)
            if u.scheme == 'http':
                connection = httplib.HTTPConnection(u.netloc)
            elif u.scheme == 'https':
                connection = httplib.HTTPSConnection(u.netloc)

            path = u.path
            connection.request('GET', path) #, headers = {'User-Agent': 'tracer-sec/osint'})
            response = connection.getresponse()
            headers = dict(response.getheaders())
            if 'location' in headers:
                # TODO: relative URLs?
                url = headers['location'] 
            else:
                break
            
            connection.close()
            response = None

        if response is not None and response.status == 200:
            data = html.fromstring(response.read())
            connection.close()
        else:
            data = None

        return data
    
    def _get_matches(self, url, paths):
        data = self._get_html(url)
        matches = []
        if data is not None:
            for path in paths:
                matches.extend(data.xpath(path))
        return matches

    def _get_links(self, url, filter = None):
        if filter is None:
            filter = ''
        else:
            filter = '[{0}]'.format(filter)
        matches = self._get_matches(url, ['//a' + filter + '/@href'])
        return list(set(matches))


if __name__ == '__main__':
    client = WebClient()
    links = client._get_links(sys.argv[1])
    print(links)
    print('\n------------------------------------\n')
    print(etree.dump(client._get__html(sys.argv[1])))

def get(config):
    return WebClient()

