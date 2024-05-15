import argparse
from datetime import datetime
from os import getenv
from json import load, dumps
from string import ascii_letters,digits 
from random import choice

import requests
from bson.objectid import ObjectId

import common
from functions import new_project

 
lettersdigits=ascii_letters+digits 
 
def random_string(n): 
   my_list = [choice(lettersdigits) for _ in range(n)] 
   my_str = ''.join(my_list) 
   return my_str

help_desc = ("Create a test project in Microreact using a JSON file as input. "
             "A data table with fake metadata will be generated automatically. "
             "The script is intended to be use directly from a command shell and has not been tested from inside a Docker container."
             )
parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument(
    "json_file",
        help=(
            "A JSON file that defines a Microreact project"
            )
        )
parser.add_argument(
    "--project_name",
    help="Project name (can be changed later in web interface)",
    default=common.USERNAME + '_' + str(datetime.now().isoformat(timespec='seconds'))
    )
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

with open(args.json_file, 'r') as f:
   json_data = load(f)

mr_access_token=common.MICROREACT_ACCESS_TOKEN
mr_base_url=common.MICROREACT_BASE_URL
verify = not args.noverify

url = mr_base_url + '/api/projects/create/?access=private'
rest_response = requests.post(
    url,
    headers= {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Token': mr_access_token
        },
    json=json_data,
    verify=verify
)

print(f"HTTP response code: {str(rest_response)}")
print(f"HTTP response content: {rest_response.content}")