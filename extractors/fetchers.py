import requests

class FetchHTTP:

    def __init__(self, url):
        self.url = url
        self.r = None

    def download(self):
        self.r = requests.get(self.url, allow_redirects=True)
        return self.r
    