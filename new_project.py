import argparse
from datetime import datetime
from pathlib import Path

import common
from functions import new_project_fn

parser = argparse.ArgumentParser(description="Create a new minimal project in Microreact using a tree and a metadata table from files.")
parser.add_argument("tree", help="Path to a Newick file containing the initial tree")
parser.add_argument("metadata", help="Path to a metadata file")
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

with open(Path(args.tree), 'r') as tree_file:
    newick = tree_file.read()

with open(Path(args.metadata), 'r') as metadata_file:
    header_line=True
    metadata_values = list()
    for line in metadata_file:
        if header_line:
            metadata_keys = line.strip().split('\t')
            print("Metadata columns:")
            print(metadata_keys)
            header_line = False
        else:
            metadata_values.append(line.strip().split('\t'))

print(f"Name of created project will be {args.project_name}")

rest_response = new_project_fn(
    project_name=args.project_name,
    initial_tree=newick,
    metadata_keys=metadata_keys,
    metadata_values=metadata_values,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"REST response: {str(rest_response)}")
print(rest_response.json())