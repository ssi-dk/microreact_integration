from json import dumps
import requests
import os
import argparse
from datetime import datetime

import classes

def stringify(value_list):
    line = ";".join([str(value) for value in value_list])
    return line + "\n"


def build_basic_project_dict(project_name: str, metadata_keys: list, metadata_values: list, tree: str):
    """
    Create a data structure that qualifies as a Microreact project and which can easily be used with the
    Microreact projects/create API endpoint to create an actual project.

    The project will contain a single tree and a data table, and will have no other elements.

    project_name: the name that will be shown for the project
    metadata_keys: keys of the metadata fields as a list. The first one will become the id field
    metadata_values: metadata values as a list of lists
    tree: tree in Newick format

    Returns: a dict structure that is validated with MR's JSON schema and can be converted to JSON with json.dumps().
    """
    project_meta = classes.Meta(name=project_name)
    id_field_name = metadata_keys[0]

    metadata_body = str()
    metadata_body += stringify(metadata_keys)  # Add keys as first line in body
    for record in metadata_values:
        metadata_body += stringify(record)

    metadata_file = classes.File(project_name=project_name, type='data', body=metadata_body)
    newick_file = classes.File(project_name=project_name, type='tree', body=tree)
    dataset = classes.Dataset(id='dataset-1', file=metadata_file.id, idFieldName=id_field_name)
    tree =  classes.Tree(
            id='tree-1',
            type='rc',
            title='Tree',
            labelField=id_field_name,
            file=newick_file.id,
            highlightedId=None
        )
    table = classes.Table(paneId='table-1', title='Metadata', columns=metadata_keys, file=metadata_file.id)

    project = classes.Project(
        meta=project_meta,
        datasets=[dataset],
        files=[metadata_file, newick_file],
        tables=[table],
        trees = [tree]
    )

    return project.to_dict()

def request_new_project(
    project_name: str,
    initial_tree: str,
    metadata_keys: list,
    metadata_values: list,
    mr_access_token: str,
    mr_base_url: str,
    public: bool=False
):
    project_as_dict = build_basic_project_dict(project_name, metadata_keys, metadata_values, initial_tree)
    json_data = dumps(project_as_dict)
    url = mr_base_url + '/api/projects/create/'
    if not public:
        url = url + '?access=private'
    rest_response = requests.post(
        url,
        headers= {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Token': mr_access_token
            },
        data=json_data,
    )
    return rest_response


if __name__ == '__main__':
    MICROREACT_BASE_URL = os.environ["MICROREACT_BASE_URL"]
    print(f"Microreact base URL: {MICROREACT_BASE_URL}")
    MICROREACT_ACCESS_TOKEN = os.environ["MICROREACT_ACCESS_TOKEN"]
    USERNAME = os.getlogin()
    print(f"OS username: {USERNAME}")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_name",
        help="Project name (can be changed later in web interface)",
        default=USERNAME + '_' + str(datetime.now().isoformat(timespec='seconds'))
        )
    args = parser.parse_args()

    print(f"Name of created project will be {args.project_name}")

#     rest_response = new_project(
#     project_name=project_name,
#     initial_tree=tree.newick,
#     metadata_keys=metadata_keys,
#     metadata_values=metadata_values,
#     mr_access_token=settings.MICROREACT_ACCESS_TOKEN,  #TODO Access-Token must be per user
#     mr_base_url=settings.MICROREACT_BASE_URL
# )
# print(rest_response)
# if rest_response.status_code == 200:
#     json_response = rest_response.json()
#     dashboard.id = json_response['id']
#     dashboard.url = json_response['url']