import sys
import httplib
import urllib
import base64
import json

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
            if target.isdigit():
                result = self.make_request('GET', '/1.1/users/show.json', { 'user_id': target, 'stringify_ids': True })
            else:
                result = self.make_request('GET', '/1.1/users/show.json', { 'screen_name': target, 'stringify_ids': True })
            
            # TODO: what if we have to look them up by id?
            self.profile_cache[result['screen_name']] = result
        return result, result['id'], result['screen_name']
        
    def get_connections(self, screen_name):
        result = []
    
        profile = self.get_profile(screen_name)[0]
        try:
            url = profile['entities']['url']['urls'][0]['expanded_url']
            result.append({ 'provider': 'web', 'task': 'profile', 'target': url, 'connection_type': 'twitter profile link' })
        except Exception as e:
            pass # profile didn't have an attached URL

        follower_data = self.get_followers(screen_name)
        try:
            followers = map(lambda x: { 'provider': 'twitter', 'task': 'profile', 'target': x, 'connection_type': 'twitter follower' }, follower_data['ids'])
            result.extend(followers)    
        except:
            # We probably got rate limited
            print(follower_data)    
        
        return result
        
    def get_text(self, screen_name):
        pass
        # bio, tweets
        
    def get_followers(self, target):
        if target.isdigit():
            return self.make_request('GET', '/1.1/followers/ids.json', { 'user_id': target, 'stringify_ids': True })
        else:
            return self.make_request('GET', '/1.1/followers/ids.json', { 'screen_name': target, 'stringify_ids': True })
        
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
    
    