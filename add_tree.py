import argparse
from pathlib import Path

import common
from functions import add_tree_fn

parser = argparse.ArgumentParser()
parser.add_argument("project_id", help="The unique ID that defines the Microreact project")
parser.add_argument("newick_file", help="Path to a Newick file containing the tree to add")
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

with open(Path(args.newick_file), 'r') as newick_file:
    newick = newick_file.read()

rest_response = add_tree_fn(
    project_id=args.project_id,
    newick=newick,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"REST response: {str(rest_response)}")
print(rest_response.json())