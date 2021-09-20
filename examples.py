from extractors import recievers, fetchers
import json
# Define content
content = {
    "name":"Joe",
    "age":"25",
    "friends":["Peter", "Stan", "Sara"], 
    "street_address": {
        "country":"Vasteras",
        "city":"Stockholm",
        "postcodes":["72213","72214"]
    }
}

#file = extentions.JSON(content=data)
#print(json.dumps(file.get_response(), indent=4, sort_keys=True))

settings = {
    "schema": {
        "type":"object",
        "properties": {
            "name":{"type":"string"},
            "age":{"type":"number"}
        }
    }
}

# Failed
file = recievers.JSON(content=content, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))


settings = {
    "type_conversion": {
        "age":"number",
        "street_address.postcodes":"number"
    }
}

# Success
file = recievers.JSON(content=content, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))


settings = {
    "type_conversion": {
        "street_address.postcodes":"number"
    },
    "schema": {
        "type":"object",
        "properties": {
            "street_address": {
                "type":"object",
                "properties": {
                    "country":{"type":"string"},
                    "city":{"type":"string"},
                    "postcodes": {
                        "type":"array",
                        "items":{"type":"number"}
                    }
                }
            }
        }
    }
}

# nested advanced conversion + schema
file = recievers.JSON(content=content, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))




# Simple download
settings = {
    "url":"https://filesamples.com/samples/code/json/sample2.json"
}

# Extractors
file = fetchers.HTTP2JSON(content=None, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))


# CSV download
settings = {
    "url":"https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
}

file = fetchers.HTTP2JSON(content=None, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))



# CSV download
settings = {
    "url":"https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv",
    "type_conversion": {
        " Identifier": "number"
    },
    "schema": {
        "type":"object",
        "properties": {
            " Identifier": {"type":"number"},
            "Username": {"type":"string"}
        }
    }
}

file = fetchers.HTTP2JSON(content=None, settings=settings)
print(json.dumps(file.get_response(), indent=4, sort_keys=True))


