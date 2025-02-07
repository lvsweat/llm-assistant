import json

class device_message:
    def __init__(self, type: str, data: dict):
        self.type = type
        self.data = data

def object_from_json(data, cls):
    json_dict = json.loads(data)
    return cls(**json_dict)