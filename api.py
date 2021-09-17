import flask
from extractors import extentions, fetchers
import csv

app = flask.Flask(__name__)
app.config["DEBUG"] = True 

@app.route('/', methods=['GET'])
def home():
    return '<h1>Hola!</h1>'

@app.route('/api/v1/extract/recieve/<int:rid>', methods=['POST'])
def recieve(rid):
    request_data = flask.request.get_json()
    file = extentions.JSON(content=request_data['content'], settings=request_data.get('settings', None))
    return file.response, file.status

@app.route('/api/v1/extract/fetch/<int:fid>', methods=['POST'])
def fetch(fid):
    # get request data
    request_data = flask.request.get_json()
    file = extentions.HTTP(content=None, settings=request_data.get('settings', None))
    return file.gen_response(), file.status

    '''
    # get request data 
    request_data = flask.request.get_json()

    # create fetch object
    file_request = fetchers.FetchHTTP(url=request_data['url'])

    # initiate download and return response
    file_response = file_request.download()

    # verify response code
    if file_response.status_code != 200:
        return 'Failed to download file from {url}'.format(url=request_data['url'])

    # TODO move file prep to extentions 
    # Determine content-type
    # If JSON
    if file_response.headers['Content-Type'] == 'application/json':
        # Try to convert file_respnse to json
        try:
            json_file = file_response.json()
        except:
            return 'Failed to convert file from {url} to json'.format(url=request_data['url'])
        # If success create json object with settings 
        file = extentions.JSON(content=json_file, settings=request_data.get('settings', None))
    # If CSV
    elif file_response.headers['Content-type'] == 'text/csv':
        # Create dict for each row
        csv_file = csv.DictReader(file_response.text.splitlines(), delimiter=',')
        #TODO add settings
        tmp_csv_settings = {'schema':{'fields':{'name':{'required':True}}}}
        # create csv object
        file = extentions.CSV(content=csv_file, settings=tmp_csv_settings)
    
    return file.errors, file.status
    '''

app.run()