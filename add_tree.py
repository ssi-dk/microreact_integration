import argparse
from pathlib import Path

import env
from functions import get_project_json_fn, update_project_fn
from classes import File, Tree

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

## We have to add something to both the files section and the trees section.
## The newick data will go into the files section.

## FILES

files = project_dict['files']
# print("Current files:")
# print(files)
# print()

new_file_instance = File(
    project_name='wkvm',  # TODO project name is not unique and not suitable for ids
    type='tree',
    body=newick)
new_file_dict = new_file_instance.to_dict()
files[new_file_instance.id] = new_file_dict
# print("files with new file added:")
# print(files)
# print()

## TREES

current_trees = project_dict.pop('trees')
# print("Current trees:")
# print(current_trees)
# print()

new_trees = dict()
for id, tree_dict in current_trees.items():
    # print(f"id: {id}  tree_dict: {tree_dict}")
    new_trees[id] = Tree(**tree_dict).to_dict()  # Crossing the river to fetch water?

# print("Trees after round-trip:")
# print(new_trees)
# print()

new_tree_id = 'some_new_tree_id'  #TODO Tree instance should det its own id like the File instance
# assert new_tree_id not in new_trees

print("File ID:")
print(new_file_dict['id'])
new_tree = Tree(id=new_tree_id, file=new_file_instance.id).to_dict()
new_trees[new_tree_id] = new_tree
# print("Trees with new tree added:")
# print(new_trees)
# print()

project_dict['trees'] = new_trees
print("Project with new tree added:")
print(project_dict)

# These two lines were added with Khalil. They must be removed later.
#files = project_dict['files']
#files['some_file_id'] = {'blob': newick, 'format': "text/x-nh", 'name': "Another tree"}

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