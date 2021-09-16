from benedict.dicts import benedict
from jsonschema import validate, exceptions as vexceptions
from tools.tools import dictSelector

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

        if self.settings:
            self.apply_settings()

    def apply_settings(self):
        if self.settings.get('type_conversion'):
            self.type_conversion() 
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


class JSON(BaseFile):

    def __init__(self, filename=None, content=None, settings=None):
        BaseFile.__init__(self, filename=filename, content=content, settings=settings)

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
                if to == 'number':
                    try: 
                        b[sub_path] = int(b[sub_path])
                    except Exception as e: 
                        self.add_error('type_conversion', str(e))
                if to == 'string':
                    try:
                        b[sub_path] = str(b[sub_path])
                    except Exception as e: 
                        self.add_error('type_conversion', str(e))
