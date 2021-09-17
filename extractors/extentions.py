from benedict.dicts import benedict
from jsonschema import validate, exceptions as vexceptions
from tools.tools import dictSelector
import ast
import requests

class BaseFile:

    def __init__(self, content=None, settings=None):
        self.content = content 
        self.settings = settings
        self.status = 201
        self.errors = {
            'schema_validation':[],
            'type_conversion':[],
        }

        if self.settings and isinstance(self, JSON):
            self.apply_settings()

    def apply_settings(self):
        if self.settings.get('type_conversion'):
            self.content = self.type_conversion() 
        if self.settings.get('schema'):
            self.validate_schema()

    def add_error(self, key, msg, status=400):
        self.status = status
        if len(self.errors[key]) <= 5:
            self.errors[key].append(msg)

    def get_response(self):
       return {
            'errors':self.errors,
            'content':self.content,
            'status':self.status,
        }

class HTTP(BaseFile): 

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
            self.status = 408
    
        if self.status == 200:
            self.convert(r)
        else:
            self.add_error('network', 'Download failed', 404)
    
    def convert(self, r):
    
        if r.headers['Content-type'] == 'application/json':

            try:
                raw_file = r.json()
            except Exception as e:
                self.add_error('network', 'Failed to convert file to JSON')
                
            file = JSON(content=raw_file, settings=self.settings)

        elif r.headers['Content-type'] == 'text/csv':

            try:
                raw_file = r.content.decode('utf-8')
            except Exception as e:
                self.add_error(str(e))

            file = CSV(content=raw_file)

        else:
            print(r.headers['Content-type'])
            self.add_error('network', 'Content-type not supported')

        self.content = file.content
        self.errors.update(file.errors)

class JSON(BaseFile):

    def __init__(self, content=None, settings=None):
        BaseFile.__init__(self, content=content, settings=settings)

    def validate_schema(self):

        try:
            validate(instance=self.content, schema=self.settings['schema'])
        except vexceptions.ValidationError as e:
            #TODO 
            # add more error context
            self.add_error('schema_validation', e.message)

    def type_conversion(self):

        b = benedict(self.content)
        path_map = dictSelector(b, key_list=self.settings['type_conversion'].keys())

        for cPath, bPath in path_map.items():
            for sub_path in bPath:
                to = self.settings['type_conversion'][cPath]

                if sub_path in b and type(b[sub_path]) in(str, int):
                    if to == 'number':
                        try: 
                            b[sub_path] = int(b[sub_path])
                        except Exception as e: 
                            self.add_error('type_conversion', str(e))
                    elif to == 'string':
                        try:
                            b[sub_path] = str(b[sub_path])
                        except Exception as e: 
                            self.add_error('type_conversion', str(e))
                    elif to in ('object', 'array'):
                        try:
                            b[sub_path] = ast.literal_eval(b[sub_path])
                        except Exception as e:
                            self.add_error('type_conversion', str(e))
                    
        return b._dict

class CSV(BaseFile):

    def __init__(self, content=None, settings=None):
        BaseFile.__init__(self, content=content, settings=settings)


    def gen_csv_file(self):
        print("lol")

    def convert_to_json(self):
        pass