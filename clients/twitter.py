import httplib
import urllib
import base64
import json
import model

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
        
    def get_node(self, target):
        if target in self.profile_cache:
            result = self.profile_cache[target]
        else:
            result = self.make_request('GET', '/1.1/users/show.json', { 'screen_name': node.name, 'stringify_ids': True })
            self.profile_cache[result['screen_name']] = result
        return model.Node('twitter', result['screen_name'], result)
    
    def get_data(self, node):
        if node.name in self.profile_cache:
            result = self.profile_cache[node.name]
        else:
            result = self.make_request('GET', '/1.1/users/show.json', { 'screen_name': node.name, 'stringify_ids': True })
            self.profile_cache[result['screen_name']] = result
        node.data = result

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

def get(config):
    return TwitterClient(config)

