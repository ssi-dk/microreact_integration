import argparse
from pathlib import Path

import env
from functions import get_project_json_fn
from classes import Tree

parser = argparse.ArgumentParser()
parser.add_argument("project_id", help="The unique ID that defines the Microreact project")
# parser.add_argument("newick_file", help="Path to a Newick file containing the tree to add")
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

# with open(Path(args.tree), 'r') as tree_file:
#     newick = tree_file.read()

rest_response = get_project_json_fn(
    project_id=args.project_id,
    mr_access_token=env.MICROREACT_ACCESS_TOKEN,
    mr_base_url=env.MICROREACT_BASE_URL,
    verify = not args.noverify
    )

json_dict = rest_response.json()
current_trees = json_dict.pop('trees')
print("Current trees:")
print(current_trees)
print()
new_trees = dict()
for id, tree_dict in current_trees.items():
    print(f"id: {id}  tree_dict: {tree_dict}")
    new_trees[id] = Tree(**tree_dict).to_dict()

# new_id = 'some_new_id'
# new_tree = Tree(id=new_id, ...).to_dict()
# new_trees[new_id] = new_tree
json_dict['trees'] = new_trees

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