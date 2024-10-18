from urllib.parse import urljoin

def construct_url(base_url, endpoint):
    return urljoin(base_url, endpoint)