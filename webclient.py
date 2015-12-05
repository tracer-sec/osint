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

class WebClient(object):
    def __init__(self, url):
        u = urlparse.urlparse(url)
        if u.scheme == 'http':
            connection = httplib.HTTPConnection(u.netloc)
        elif u.scheme == 'https':
            connection = httplib.HTTPSConnection(u.netloc)

        path = u.path
        connection.request('GET', path) #, headers = {'User-Agent': 'tracer-sec/osint'})
        response = connection.getresponse()

        # TODO: handle 3xx

        if response.status == 200:
            self._html = html.fromstring(response.read())
        else:
            self._html = ''

        connection.close()

    def get_matches(self, paths):
        matches = []
        for path in paths:
            matches.extend(self._html.xpath(path))
        return matches

    def get_links(self, filter = None):
        if filter is None:
            filter = ''
        else:
            filter = '[{0}]'.format(filter)
        matches = self.get_matches(['//a' + filter + '/@href'])
        return list(set(matches))

    
if __name__ == '__main__':
    client = WebClient(sys.argv[1])
    links = client.get_links()
    print(links)
    print('\n------------------------------------\n')
    print(etree.dump(client._html))


