import os
from jsonschema import validate
from json import loads
from pathlib import Path

MICROREACT_BASE_URL = os.environ["MICROREACT_BASE_URL"]
MICROREACT_ACCESS_TOKEN = os.environ["MICROREACT_ACCESS_TOKEN"]
USERNAME =  os.environ["USER"]

current_dir = Path(__file__).parent
with open(Path(current_dir, 'microreact_project_schema_v1.json'), 'r') as schema_file:
    MR_PROJECT_SCHEMA = loads(schema_file.read())

def validate_json(json_dict:dict):
    return validate(json_dict, MR_PROJECT_SCHEMA)