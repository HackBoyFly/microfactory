from benedict.dicts import benedict
from jsonschema import validate, exceptions as vexceptions
from tools.tools import dictSelector
import ast
import csv

class BaseFile:

    def __init__(self, content=None, settings=None):
        self.content = content
        self.settings = settings
        self.status = 201
        self.errors = {
            'schema_validation': [],
            'type_conversion': [],
            'file_conversion': []
        }

        # If instance is JSON apply settings
        if self.settings and isinstance(self, JSON):
            self.apply_settings()

    def apply_settings(self):
        if self.settings.get('type_conversion'):
            self.type_conversion()
        if self.settings.get('schema'):
            self.validate_schema()

    def add_error(self, key, msg, status=400):
        self.status = status
        if len(self.errors[key]) <= 5:
            self.errors[key].append(msg)

    def get_response(self):
        return {
            'errors': self.errors,
            'content': self.content,
            'status': self.status,
        }

    def merge_dict(self, d1, d2):
        final = {}
        dicts = [d1, d2]  # x and y are each dicts defined by op

        for D in dicts:
            for key, value in D.items():
                if key not in final:
                    final[key] = []
                for v in value:
                    final[key].append(v)
        return final


class JSON(BaseFile):

    def __init__(self, content=None, settings=None):
        BaseFile.__init__(self, content=content, settings=settings)

    def validate_schema(self):

        schema = self.settings['schema']
        # if content is list-based, fix paths
        if 'jsonlist' in self.content:
            schema = {
                'type': 'object',
                'properties': {
                    'jsonlist': {
                        'type': 'array',
                        'items': schema
                    }
                }
            }

        try:
            validate(instance=self.content, schema=schema)
        except vexceptions.ValidationError as e:
            # TODO
            # add more error context
            self.add_error('schema_validation', e.message)

    def type_conversion(self):

        tc = self.settings['type_conversion']
        # if content is list-based, fix paths
        tc = {'jsonlist.'+k: v for k,
              v in tc.items()} if 'jsonlist' in self.content else tc

        
        # Create benedict dict
        b = benedict(self.content)
        # Get all possible paths in dict and generate {clean.path:[clean.path[0],..]}
        path_map = dictSelector(b, key_list=tc.keys())
        # Loop through path_map and convert values
        for cPath, bPath in path_map.items():
            for sub_path in bPath:
                to = tc[cPath]
                if sub_path in b and type(b[sub_path]) in (str, int):
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

        self.content = b._dict


class CSV(BaseFile):

    def __init__(self, content=None, settings=None, file=None, delimiter=','):
        self.delimiter = delimiter
        BaseFile.__init__(self, content=content, settings=settings)

        if file: 
            with open('test.csv', 'r') as csvfile:
                self.content = csvfile.read()
                
        self.gen_csv_file()

    def gen_csv_file(self):

        try:
            self.content = self.content.decode('utf-8')
        except Exception as e:
            self.add_error('file_conversion', 'Failed to decode csv utf-8')
        
        cdict = csv.DictReader(self.content.splitlines(), delimiter=self.delimiter)
        jdict = {'jsonlist': [d for d in cdict]}
        self.convert_to_json(jdict)

    def convert_to_json(self, jdict):

        json = JSON(content=jdict, settings=self.settings)
        
        self.content = json.content['jsonlist']
        self.errors = self.merge_dict(self.errors, json.errors)
        self.status = json.status

