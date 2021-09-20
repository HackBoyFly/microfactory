from .recievers import BaseFile, JSON, CSV
import requests

class HTTP2JSON(BaseFile):

    def __init__(self, content=None, settings=None):
        BaseFile.__init__(self,  content=content, settings=settings)
        self.errors['network'] = []
        self.download(self.settings['url'])

    def download(self, url):
        # TODO catch timeout
        try:
            r = requests.get(url, allow_redirects=True, timeout=30)
            self.status = r.status_code
        except Exception as e:
            self.add_error('network', 'Timeout request', 408)

        if self.status == 200:
            self.convert(r)
        else:
            self.add_error('network', 'Download failed', 404)

    def convert(self, r):
        ct = r.headers['Content-type']
        if ct == 'application/json':
            try:
                raw_file = r.json()
            except Exception as e:
                self.add_error('network', 'Failed to convert file to JSON')

            file = JSON(content=raw_file, settings=self.settings)

        elif ct:
            try:
                raw_file = r.content.decode('utf-8')
            except Exception as e:
                self.add_error(str(e))

            file = CSV(content=raw_file, settings=self.settings)

        else:
            self.add_error(
                'network', 'Content-type not supported {ct}'.format(ct=ct))

        self.content = file.content
        self.errors.update(file.errors)
        self.status = file.status