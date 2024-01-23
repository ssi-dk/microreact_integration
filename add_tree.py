import argparse
from pathlib import Path

import env
# from functions import add_tree_fn

parser = argparse.ArgumentParser()
parser.add_argument("project_id", help="The unique ID that defines the Microreact project")
parser.add_argument("tree", help="Path to a Newick file containing the tree to add")
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

with open(Path(args.tree), 'r') as tree_file:
    newick = tree_file.read()

# rest_response = add_tree_fn(
#     project_id=args.project_id,
#     initial_tree=newick,
#     new_tree=args.tree,
#     mr_access_token=env.MICROREACT_ACCESS_TOKEN,
#     mr_base_url=env.MICROREACT_BASE_URL,
#     verify = not args.noverify
#     )
# print(f"REST response: {str(rest_response)}")
# print(rest_response.json())