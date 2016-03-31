import sys
import model

client = None

def get_twitter_profile(node):
    n = client.get_node(node.name)
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
    data = client.get_followers(node.name)

    if type(data) is str:
        return []
    else:
        return map(lambda x: model.Node('twitter', x['screen_name'], x), data['users'])
    
def get(config, c):
    global client
    client = c

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
    
