import httplib
import json
import model

client = None

class GithubClient(object):
    def __init__(self):
        pass # oauth not really necessary if we're just doing queries
        
    def get_profile(self, username):
        result = self.make_request('GET', '/users/{0}'.format(username), {})
        if result is None:
            return None
        else:
            return model.Node('github', result['login'], { 'profile': result })
            
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

            
def get_github_profile(node):
    n = client.get_profile(node.name)
    if n is None:
        return []
    else:
        return [n]
        
        
def get_github_url(node):
    if 'profile' in node.data and 'blog' in node.data['profile'] and node.data['profile']['blog'] is not None:
        return [model.Node('website', node.data['profile']['blog'])]
    else:
        return []
        
        
def get_github_followers(node):
    # should probably just use followers_url in node.data
    data = client.get_followers(node.name)
    if data is None:
        return []
    else:
        result = map(lambda x: model.Node('github', x['login'], { 'profile': x }), data)
        return result


def get(config):
    global client
    client = GithubClient()
    
    return [
        {
            'func': get_github_profile,
            'name': 'Github profile',
            'acts_on': ['person']
        },
        {
            'func': get_github_url,
            'name': 'Github blog URL',
            'acts_on': ['github']
        },
        {
            'func': get_github_followers,
            'name': 'Github followers',
            'acts_on': ['github']
        }
    ]
    