import sys
import httplib
import urllib
import json

class RedditClient(object):
    def __init__(self, config):
        self.access_token = None
        auth_header = 'Basic ' + config['api_key'] + ':' + config['api_secret']
        body = urllib.urlencode({ 'grant_type': 'password', 'username': config['username'], 'password': config['password'] })
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': auth_header
        }
        connection = httplib.HTTPSConnection('ssl.reddit.com')
        connection.request('POST', '/api/v1/access_token', body, headers)
        response = connection.getresponse()
        if response.status == 200:
            response_data = json.load(response)
            self.access_token = response_data['access_token']
            print(self.access_token)
        else:
            print('{0} {1}'.format(response.status, response.reason))
        connection.close()
        
    def get_profile(self, username):
        return self.make_request('GET', '/user/{0}/about.json'.format(username), {})
        
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
            return json.load(response)
        else:
            return '{0} {1}'.format(response.status, response.reason)
        


if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    
    client = RedditClient(config['reddit'])
    if client.access_token != None:
        print(client.get_profile(username))
    
    