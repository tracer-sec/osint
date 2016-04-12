import model
import httplib
import json

class RedditClient(object):
    def __init__(self):
        pass # oauth not really necessary if we're just doing queries
        
    def get_profile(self, username):
        result = self.make_request('GET', '/user/{0}/about.json'.format(username), {})
        if 'kind' in result:
            del result['kind']
        if 'data' in result and 'name' in result['data']:
            return model.Node('reddit', result['data']['name'], result)
        else:
            return None
        
    def make_request(self, method, url, params):
        connection = httplib.HTTPSConnection('www.reddit.com')
        connection.request(method, url)
        response = connection.getresponse()
        if response.status == 200:
            return json.load(response)
        else:
            return '{0} {1}'.format(response.status, response.reason)


def get(config):
    return RedditClient()

