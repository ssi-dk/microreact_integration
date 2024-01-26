import argparse
from pathlib import Path

import env
from functions import get_project_json_fn, update_project_fn
from classes import Tree

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

rest_response = get_project_json_fn(
    project_id=args.project_id,
    mr_access_token=env.MICROREACT_ACCESS_TOKEN,
    mr_base_url=env.MICROREACT_BASE_URL,
    verify = not args.noverify
    )

project_dict = rest_response.json()
current_trees = project_dict.pop('trees')
# print("Current trees:")
# print(current_trees)
# print()

new_trees = dict()
for id, tree_dict in current_trees.items():
    # print(f"id: {id}  tree_dict: {tree_dict}")
    new_trees[id] = Tree(**tree_dict).to_dict()

# print("Trees after round-trip:")
# print(new_trees)
# print()

new_id = 'some_new_id'  #TODO make an algorithm that can generate a reeasonable unique id
# assert new_id not in new_trees

new_tree = Tree(id=new_id, file='some_file_id').to_dict()
new_trees[new_id] = new_tree
# print("Trees with new tree added:")
# print(new_trees)
# print()

project_dict['trees'] = new_trees
# print("Project with new tree added:")
# print(project_dict)

files = project_dict['files']
files['some_file_id'] = {'blob': newick, 'format': "text/x-nh", 'name': "Another tree"}

rest_response = update_project_fn(
    project_id=args.project_id,
    project_dict=project_dict,
    mr_access_token=env.MICROREACT_ACCESS_TOKEN,
    mr_base_url=env.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
# print(f"REST response: {str(rest_response)}")
# print(rest_response.json())

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