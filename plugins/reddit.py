import sys
import httplib
import urllib
import json

class RedditClient(object):
    def __init__(self):
        pass # oauth not really necessary if we're just doing queries
        
    def get_profile(self, username):
        result = self.make_request('GET', '/user/{0}/about.json'.format(username), {})
        return result, result['id'], result['name']
        
    def get_connections(self, screen_name):
        # friends?
        # urls?
        return []
        
    def make_request(self, method, url, params):
        connection = httplib.HTTPSConnection('www.reddit.com')
        connection.request(method, url, headers=headers)
        response = connection.getresponse()
        if response.status == 200:
            return json.load(response)
        else:
            return '{0} {1}'.format(response.status, response.reason)


def get(config):
    return RedditClient()
    
    