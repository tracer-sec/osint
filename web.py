import whois
import utils

class WebClient(object):
    def __init__(self):
        pass
        
    def get_profile(self, target):
        domain = utils.get_domain_from_url(target)
        whois_info = whois.lookup(domain, True)
        data = { 'whois': whois_info }
        return data, target, target
        
    def get_connections(self, target):
        return []
        