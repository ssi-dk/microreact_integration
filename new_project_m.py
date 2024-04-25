import argparse
from datetime import datetime
from pathlib import Path
from os import getenv
from sys import exit

import pymongo
from bson.objectid import ObjectId

import common
from functions import new_project_fn

help_desc = ("Create a new minimal project in Microreact using a tree from MongoDB. "
             "The script assumes a local MongoDB instance is running on default port and with no authentication requirements. "
             "The MongoDB instance must contain a database named 'bio_api_test' containing a collection named 'tree_calculations.' "
             "A minimal metadata file will be generated automatically.")
parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument("--tree_calc", help="Mongo ID for a document in tree_calculations with the tree to send to Microreact")
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
if args.tree_calc is not None:
    tree_calc = db['tree_calculations'].find_one({'_id': ObjectId(args.tree_calc)})
else:
    tree_calc = db['tree_calculations'].find_one()
print("Full tree calc document:")
print(tree_calc)
dmx_job = db['dist_calculations'].find_one({'_id': ObjectId(tree_calc['dmx_job'])})
print("DMX job document:")
print(dmx_job)
seq_to_mongo:dict = dmx_job['result']['seq_to_mongo']
print("Seq to mongo:")
print(seq_to_mongo)
metadata_keys = ['seq_id', 'db_id']
metadata_values = list()
for k, v in seq_to_mongo.items():
    metadata_values.append([k, v])

rest_response = new_project_fn(
    project_name=args.project_name,
    initial_tree=tree_calc['result'],
    metadata_keys=metadata_keys,
    metadata_values=metadata_values,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"REST response: {str(rest_response)}")
print(rest_response.json())