import requests

class FetchHTTP:

    def __init__(self, url):
        self.url = url
        self.extention = self.get_pre_content_type() 
        self.filename = self.get_filename()
        self.r = None

    def download(self):
        self.r = requests.get(self.url, allow_redirects=True)
        return self.r

    def get_pre_content_type(self):
        return self.url.split('/')[-1].split('.')[1]

    def get_filename(self):
        return self.url.split('/')[-1].split('.')[0]

    def save_file(self, filename=None, extention=None, path=None):

        # TODO: Add path logic, move to separate func/class

        if filename:
            self.filename = filename
        if extention:
            self.extention = extention
 
        open(self.filename+'.'+self.extention, 'wb').write(self.r.content)
    