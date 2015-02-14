import sys
import httplib
import urllib
import json
import model

client = None

class RedditClient(object):
    def __init__(self):
        pass # oauth not really necessary if we're just doing queries
        
    def get_profile(self, username):
        result = self.make_request('GET', '/user/{0}/about.json'.format(username), {})
        return model.Node('reddit', result['data']['name'], result)
        
    def make_request(self, method, url, params):
        connection = httplib.HTTPSConnection('www.reddit.com')
        connection.request(method, url)
        response = connection.getresponse()
        if response.status == 200:
            return json.load(response)
        else:
            return '{0} {1}'.format(response.status, response.reason)

            
def get_profile(node):
    n = client.get_profile(node.name)
    return [n]
    
def get_stats(node):
    response = client.make_request('GET', '/user/{0}/overview.json?sort=top&limit=100'.format(node.name), {})
    data = response['data']['children']
    
    result = {
        'average_score': 0,
        'min_score': 9999999,
        'max_score': 0,
        'subreddit_activity': {},
        'link_domains': []
    }
    
    for entry in data:
        subreddit = entry['data']['subreddit']
        if 'domain' in entry['data'] and not entry['data']['is_self']:
            domain = entry['data']['domain']
        else:
            domain = None
        score = entry['data']['score']
        if subreddit in result['subreddit_activity']:
            result['subreddit_activity'][subreddit] = result['subreddit_activity'][subreddit] + 1
        else:
            result['subreddit_activity'][subreddit] = 1
        if domain is not None and domain not in result['link_domains']:
            result['link_domains'].append(domain)
        result['min_score'] = min(result['min_score'], score)
        result['max_score'] = max(result['max_score'], score)
        result['average_score'] = result['average_score'] + score
    
    result['average_score'] = float(result['average_score']) / len(data)
    node.data['stats'] = result
    return []
    

def get(config):
    global client
    client = RedditClient()
    
    return [
        {
            'func': get_profile,
            'name': 'Reddit profile',
            'acts_on': ['person']
        },
        {
            'func': get_stats,
            'name': 'Reddit stats',
            'acts_on': ['reddit']
        }       
    ]
    