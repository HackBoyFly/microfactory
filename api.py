import flask
from werkzeug.wrappers import request
from extractors import extentions, fetchers


app = flask.Flask(__name__)
app.config["DEBUG"] = True 

@app.route('/', methods=['GET'])
def home():
    return '<h1>Hola!</h1>'

@app.route('/api/v1/r/<int:rid>', methods=['POST'])
def recieve(rid):
    request_data = flask.request.get_json()
    _file = extentions.JSON(_file=request_data)
    return ''

@app.route('/api/v1/f/<int:fid>', methods=['POST'])
def fetch(fid):
    request_data = flask.request.get_json()
    url = request_data['url']
    filename = request_data.get('filename', None)
    extention = request_data.get('extention', None)
    file_request = fetchers.FetchHTTP(url=url)
    file_request.download()
    file_request.save_file(filename=filename, extention=extention)

    return ''

app.run()