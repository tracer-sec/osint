import model

client = None

def get_github_profile(node):
    n = client.get_node(node.name)
    if n is None:
        return []
    else:
        return [n]

        
def get_github_url(node):
    if 'profile' in node.data and 'blog' in node.data['profile'] and node.data['profile']['blog'] is not None and len(node.data['profile']['blog']) > 0:
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


def get(config, c):
    global client
    client = c
    
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
    
