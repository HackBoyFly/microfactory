import requests
from werkzeug.wrappers import request
from extractors import extentions

class FetchHTTP:

    def __init__(self, request_data):
        self.request_data = request_data
        self.content_type = None
        self.response = {
            "errors":{"response":[], "conversion":[]},
            "status":None,
            "request_data":request_data,
            "content_type":None,
            "file": None
        }
        self.download()

    def download(self):

        self.r = requests.get(self.request_data['url'], allow_redirects=True)
        self.status = self.r.status_code

        if self.status != 200:
            self.response['errors']['response'].append('Download request failed')
        else:
            self.response['content_type'] = self.r.headers['Content-type']

    def convert_to_file(self):
        
        if self.response['content_type'] == 'application/json':

            try:
                self.content = self.r.json()
            except Exception as e: 
                 self.response['errors']['conversion'].append(str(e))

            self.response['file'] = extentions.JSON(
                content=self.content, settings=self.request_data.get('settings', None)
                ).response

