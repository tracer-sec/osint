import urlparse

def get_domain(s):
    if '@' in s:
        # it's an email address
        domain = s[s.index('@') + 1:]
    else:
        result = urlparse.urlparse(s)
        domain = result.netloc
    return domain
    