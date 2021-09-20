# microfactory
microfactory is a liteweight ETL API and libary written in Python.

## Features
**Extract**
- Support for JSON, CSV
- File download
- Schema validation for all filetypes
- Type conversion for all filetypes
- TBD

**Transform**
- TBD

**Load**
- TBD

## Usage
### Basic extentions
```python
from microfactory.extractors import extentions

# Define content
data = {
  "content": {
    "name":"Joe",
    "age":25
    "friends":["Peter", "Stan", "Sara"]
  }
}

file = extentions.JSON(content=data)
print(file.content)
```

### Extentions with schema validation
```python
from microfactory.extractors import extentions

# Define settings
{"settings":{
    "schema": {
      "type":"object",
        "properties": {
          "name":{"type":"string"},
          "age":{"type":"number"},
          "friends": {
            "type":"array",
            "items":{"type":"string"}
          }
        }
      }
    }
  }
}
file = extentions.JSON(content=data)
print(file.content)
