import urlparse

def get_domain_from_url(url):
    result = urlparse.urlparse(url)
    return result.netloc
    