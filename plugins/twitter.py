import sys
import httplib
import urllib
import base64
import json
import model

client = None

class TwitterClient(object):
    def __init__(self, config):
        self.access_token = None
        self.profile_cache = {}
        
        auth_header = 'Basic ' + base64.b64encode(config['api_key'] + ':' + config['api_secret'])
        body = urllib.urlencode({ 'grant_type': 'client_credentials' })
        headers = { 
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': auth_header
        }
        connection = httplib.HTTPSConnection('api.twitter.com')
        connection.request('POST', '/oauth2/token', body, headers)
        response = connection.getresponse()
        if response.status == 200:
            response_data = json.load(response)
            self.access_token = response_data['access_token']
            #print(self.access_token)
        else:
            print('{0} {1}'.format(response.status, response.reason))
        connection.close()
        
    def get_profile(self, target):
        if target in self.profile_cache:
            result = self.profile_cache[target]
        else:
            result = self.make_request('GET', '/1.1/users/show.json', { 'screen_name': target, 'stringify_ids': True })
            self.profile_cache[result['screen_name']] = result
        return model.Node('twitter', result['screen_name'], result)
        
    def get_text(self, screen_name):
        pass
        # bio, tweets
                
    def get_lists(self, screen_name):
        return self.make_request('GET', '/1.1/lists/list.json', { 'screen_name': screen_name })
        
    def make_request(self, method, url, params):
        connection = httplib.HTTPSConnection('api.twitter.com')
        headers = { 'Authorization': 'Bearer ' + self.access_token }
        body = urllib.urlencode(params)
        if method == 'POST':
            headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
            connection.request(method, url, body, headers)
        elif method == 'GET':
            if len(body) > 0:
                url = url + '?' + body
            connection.request(method, url, headers=headers)
        response = connection.getresponse()
        if response.status == 200:
            result = json.load(response)
        else:
            result = '{0} {1}'.format(response.status, response.reason)
        connection.close()
        return result

        
def get_twitter_profile(node):
    n = client.get_profile(node.name)
    if n is None:
        return []
    else:
        return [n]
    
def get_twitter_url(node):
    try:
        url = node.data['entities']['url']['urls'][0]['expanded_url']
    except KeyError:
        return []

    n = model.Node('website', url, {})
    # what site data to grab?
    return [n]
    
def get_twitter_followers(node):
    data = client.make_request('GET', '/1.1/followers/list.json', { 'screen_name': node.name, 'skip_status': True, 'include_user_entities': True })
    if type(data) is str:
        return []
    else:
        return map(lambda x: model.Node('twitter', x['screen_name'], x), data['users'])
    
def get(config):
    global client
    client = TwitterClient(config)

    return [
        {
            'func': get_twitter_profile,
            'name': 'Twitter profile',
            'acts_on': ['person']
        },
        {
            'func': get_twitter_url,
            'name': 'Twitter profile URL',
            'acts_on': ['twitter']
        },
        {
            'func': get_twitter_followers,
            'name': 'Twitter followers',
            'acts_on': ['twitter']
        }
    ]
    