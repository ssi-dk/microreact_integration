import argparse
from datetime import datetime
from pathlib import Path
from os import getenv
from sys import exit

import pymongo
from bson.objectid import ObjectId

import common
from functions import new_project

help_desc = ("Create a new project in Microreact using one or more trees defined in MongoDB. "
             "The script assumes a local MongoDB instance is running on default port and with no authentication requirements. "
             "The MongoDB instance must contain a database named 'bio_api_test' containing a collection named 'tree_calculations.' "
             "A minimal data table will be generated automatically.")
parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument(
    "--trees",
        help=(
            "Mongo ID(s) for document(s) in tree_calculations collection. "
            "If more than one ID, separate with commas without spaces. "
            "If argument is omitted, a random tree tree_calculations collection will be chosen."
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
if trees_str is None:
    tc = db['tree_calculations'].find_one()
    dmx_job_id = tc['dmx_job']
    dmx_job = db['dist_calculations'].find_one({'_id': ObjectId(dmx_job_id)})
    assert 'result' in dmx_job
    assert type(dmx_job['result']) is dict
    assert['seq_to_mongo'] in dmx_job['result']
    print(dmx_job)
    tree_calcs.append(tc)
else:
    tree_ids = [ ObjectId(id) for id in trees_str.split(',') ]
    print("Tree ids:")
    print(tree_ids)
    tree_cursor = db['tree_calculations'].find({'_id': {'$in': tree_ids}})
    tc = next(tree_cursor)
    tree_calcs.append(tc)
    dmx_job_id = tc['dmx_job']
    dmx_job = db['dist_calculations'].find_one({'_id': ObjectId(dmx_job_id)})
    while True:
        try:
            tc = next(tree_cursor)
            # Make sure that all trees are calculated from the same dmx job
            assert tc['dmx_job'] == dmx_job_id
            tree_calcs.append(tc)
        except StopIteration:
            break

seq_to_mongo:dict = dmx_job['result']['seq_to_mongo']
print("Seq to mongo:")
print(seq_to_mongo)
metadata_keys = ['seq_id', 'db_id']
metadata_values = list()
for k, v in seq_to_mongo.items():
    metadata_values.append([k, v])

rest_response = new_project(
    project_name=args.project_name,
    tree_calcs=tree_calcs,
    metadata_keys=metadata_keys,
    metadata_values=metadata_values,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"REST response: {str(rest_response)}")
print(rest_response.json())