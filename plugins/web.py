import whois
import httplib
import urlparse
import utils

class WebClient(object):
    def __init__(self):
        pass
        
    def get_profile(self, target):
        domain = utils.get_domain_from_url(target)
        whois_info = whois.lookup(domain, True)
        data = { 'whois': whois_info }
        
        # server, meta description . . .
        u = urlparse.urlparse(target)
        if u.scheme == 'http':
            connection = httplib.HTTPConnection(u.netloc)
        elif u.scheme == 'https':
            connection = httplib.HTTPSConnection(u.netloc)
            
        connection.close()
        
        return data, target, target
        
    def get_connections(self, target):
        # Emails for administrative contacts?
        return []
        
def get(config):
    return WebClient()
    