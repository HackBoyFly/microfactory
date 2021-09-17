from benedict.dicts import benedict
from jsonschema import validate, exceptions as vexceptions
from tools.tools import dictSelector
import ast

class BaseFile:

    def __init__(self, filename=None, content=None, settings=None):
        self.filename = filename
        self.content = content 
        self.settings = settings
        self.status = 201
        self.errors = {
            'schema_validation':[],
            'type_conversion':[]
        }
        self.response = {
            'errors':self.errors,
            'content':self.content,
            'status':self.status
        }

        if self.settings:
            self.apply_settings()

    def apply_settings(self):
        if self.settings.get('type_conversion'):
            self.content = self.type_conversion() 
        if self.settings.get('schema'):
            self.validate_schema()

    def add_error(self, key, msg):
        self.status = 400
        if len(self.errors[key]) <= 5:
            self.errors[key].append(msg)
  

class CSV(BaseFile):

    def __init__(self, filename=None, content=None, settings=None):
        print(content)
        BaseFile.__init__(self, filename=filename, content=content, settings=settings)
        self.extention = 'JSON'

    def validate_schema(self):
        print("No schema validation for csv")
        for row in self.content:
            print(row)

    def convert_to_json(self):
        #TODO 
        # Convert CSV to json 
        # Move schema and convert to basefile
        pass 

class JSON(BaseFile):

    def __init__(self, filename=None, content=None, settings=None):
        BaseFile.__init__(self, filename=filename, content=content, settings=settings)

    def validate_schema(self):

        # Move to base file

        try:
            validate(instance=self.content, schema=self.settings['schema'])
        except vexceptions.ValidationError as e:
            #TODO 
            # add more error context
            self.add_error('schema_validation', e.message)

    def type_conversion(self):

        # Moveto base file

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
