import httplib
import json
import model

class GithubClient(object):
    def __init__(self, config):
        pass # oauth not really necessary if we're just doing queries
        
    def get_node(self, username):
        result = self.make_request('GET', '/users/{0}'.format(username), {})
        if result is None:
            return None
        else:
            return model.Node('github', result['login'], { 'profile': result })

    def get_data(self, node):
        result = self.make_request('GET', '/users/{0}'.format(node.name), {})
        if result is None:
            node.data = {}
        else:
            node.data = { 'profile': result }
        
    def get_followers(self, username):
        result = self.make_request('GET', '/users/{0}/followers'.format(username), {})
        return result
        
    def make_request(self, method, url, params):
        connection = httplib.HTTPSConnection('api.github.com')
        connection.request(method, url, headers = {'User-Agent': 'tracer-sec/osint', 'Accept': 'application/vnd.github.v3+json'})
        response = connection.getresponse()
        if response.status == 200:
            return json.load(response)
        else:
            return None

def get(config):
    return GithubClient(config)

