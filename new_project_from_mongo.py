import argparse
from datetime import datetime
from os import getenv
from json import dumps
from string import ascii_letters,digits 
from random import choice

import pymongo
from bson.objectid import ObjectId

import common
from functions import new_project

 
lettersdigits=ascii_letters+digits 
 
def random_string(n): 
   my_list = [choice(lettersdigits) for _ in range(n)] 
   my_str = ''.join(my_list) 
   return my_str

help_desc = ("Create a test project in Microreact using one or more trees and some dummy data. "
             "The script depends on a MongoDB database defined by BIO_API_MONGO_CONNECTION, or in the case this environment "
             "variable is not set, a MongoDB database on mongodb://mongodb:27017/bio_api_test. "
             "A data table with fake metadata will be generated automatically. "
             "The script is intended to be use directly from a command shell and has not been tested from inside a Docker container."
             )
parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument(
    "trees",
        help=(
            "Mongo ID(s) for document(s) in tree_calculations collection. "
            "If more than one ID, separate with commas without spaces. "
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

connection_string = getenv('BIO_API_MONGO_CONNECTION', 'mongodb://mongodb:27017/bio_api_test')
connection:pymongo.MongoClient = pymongo.MongoClient()
db = connection.get_database('bio_api_test')
trees_str: str = args.trees
tree_calcs = list()
tree_ids = [ ObjectId(id) for id in trees_str.split(',') ]
print("Tree ids:")
print(tree_ids)
tree_cursor = db['tree_calculations'].find({'_id': {'$in': tree_ids}})
tc = next(tree_cursor)
tree_calcs.append(tc)
dmx_job_id = tc['dmx_job']  #TODO unify
dmx_job = db['dist_calculations'].find_one({'_id': ObjectId(dmx_job_id)})
assert 'result' in dmx_job
assert type(dmx_job['result']) is dict
assert 'seq_to_mongo' in dmx_job['result']
while True:
    try:
        tc = next(tree_cursor)
        # Make sure that all trees are calculated from the same dmx job
        assert tc['dmx_job'] == dmx_job_id
        tree_calcs.append(tc)
    except StopIteration:
        break

# Create minimal metadata set
seq_to_mongo:dict = dmx_job['result']['seq_to_mongo']
metadata_keys = ['seq_id', 'db_id']

metadata_values = list()
for k, v in seq_to_mongo.items():
    metadata_values.append([k, str(v)])

# Add fake encrypted metadata
metadata_keys.extend(['cpr', 'navn', 'mk', 'alder', 'landnavn', 'kmanavn'])
row: list
for row in metadata_values:
    for n in range(6):
        row.append(random_string(10))

# Add URL fields
metadata_keys.extend(['cpr__url', 'navn__url', 'mk__url', 'alder__url', 'landnavn__url', 'kmanavn__url'])
row: list
for row in metadata_values:
    for n in range(6):
        row.append('https://test.sofi-platform.dk/')

print("Metadata keys:")
print(metadata_keys)
print()
print("Metadata values:")
print(metadata_values)

rest_response = new_project(
    project_name=args.project_name,
    tree_calcs=tree_calcs,
    metadata_keys=metadata_keys,
    metadata_values=metadata_values,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"HTTP response code: {str(rest_response)}")
print("Response as actual JSON:")
print(dumps(rest_response.json()))