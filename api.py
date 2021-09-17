import flask
from extractors import extentions

app = flask.Flask(__name__)
app.config["DEBUG"] = True 

@app.route('/', methods=['GET'])
def home():
    return '<h1>Hola!</h1>'

@app.route('/api/v1/extract/recieve/<int:rid>', methods=['POST'])
def recieve(rid):
    request_data = flask.request.get_json()
    file = extentions.JSON(content=request_data['content'], settings=request_data.get('settings', None))
    return file.get_response(), file.status

@app.route('/api/v1/extract/fetch/<int:fid>', methods=['POST'])
def fetch(fid):
    # get request data
    request_data = flask.request.get_json()
    file = extentions.HTTP(content=None, settings=request_data.get('settings', None))
    return file.get_response(), file.status

app.run()