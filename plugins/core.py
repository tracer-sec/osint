import re
import model

SOCIAL_MEDIA_URLS = {
    'twitter': 'https?://twitter.com/([A-Za-z0-9_-]+)',
    'github': 'https?://github.com/([A-Za-z0-9_-]+)'
}

EMAIL_PATTERN = '[A-Za-z0-9._-]+@[A-Za-z0-9._-]+\.[A-Za-z]+'

def find_matches(d, regex):
    result = []
    for key in d.keys():
        if type(d[key]) == str or type(d[key]) == unicode:
            matches = regex.findall(d[key])
            result.extend(matches)
        elif type(d[key]) == dict:
            result.extend(find_matches(d[key], regex))
    return result


def get_social_links(node):
    result = []
    for r in SOCIAL_MEDIA_URLS.keys():
        urls = find_matches(node.data, SOCIAL_MEDIA_URLS[r])
        result.extend(map(lambda x: model.Node(r, x), urls))
    print(result)
    return result

            
def get_emails(node):
    regex = re.compile(EMAIL_PATTERN)
    result = find_matches(node.data, regex)
    return map(lambda x: model.Node('email', x), set(result))


for r in SOCIAL_MEDIA_URLS.keys():
    SOCIAL_MEDIA_URLS[r] = re.compile(SOCIAL_MEDIA_URLS[r])


if __name__ == '__main__':
    n = model.Node('foo', 'bar')
    n.data = {
        'foo': 'bar@test.com',
        'this': {
            'a': 'what is test@example.org going on here',
            'b': 'lorem ipsum@example asdasdasd'
        },
        'lol': 123,
        'kek': {
            'asdasd': 123.12,
            'asdasf': {
                'poiasd': 'asdkjasd test@example.org as da dasda',
                'poihjl': 'asdlksajdklsajdkl https://github.com/tracer-sec sajdlasjd las da'
            }
        }
    }
    result = get_emails(n)
    print(result)
    result = get_social_links(n)
    print(result)


def get(config):
    return [
        {
            'func': get_social_links,
            'name': 'Hoover up social links',
            'acts_on': ['*']
        },
        {
            'func': get_emails,
            'name': 'Look for email addresses',
            'acts_on': ['*']
        }
    ]
    
