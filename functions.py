from json import dumps
import requests

import classes
from common import validate_json

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

    metadata_file = classes.File(type='data', body=metadata_body)
    newick_file = classes.File(type='tree', body=tree)
    dataset = classes.Dataset(file=metadata_file.id, idFieldName=id_field_name)
    tree =  classes.Tree(
            type='rc',
            title='Tree',
            labelField=id_field_name,
            file=newick_file.id,
            highlightedId=None
        )
    table = classes.Table(title='Metadata', columns=metadata_keys, file=metadata_file.id)

    project = classes.Project(
        meta=project_meta,
        datasets=[dataset],
        files=[metadata_file, newick_file],
        tables=[table],
        trees = [tree]
    )

    return project.to_dict()

def new_project_fn(
    project_name: str,
    initial_tree: str,
    metadata_keys: list,
    metadata_values: list,
    mr_access_token: str,
    mr_base_url: str,
    public: bool=False,
    verify: bool=True
):
    project_dict = build_basic_project_dict(project_name, metadata_keys, metadata_values, initial_tree)
    json_data = dumps(project_dict)
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
        verify=verify
    )
    return rest_response

def get_project_json_fn(
    project_id: str,
    mr_access_token: str,
    mr_base_url: str,
    verify: bool=True
):
    url = mr_base_url + '/api/projects/json?project=' + project_id
    rest_response = requests.get(
        url,
        headers= {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Token': mr_access_token
            },
        verify=verify
    )
    return rest_response

def update_project_fn(
    project_id: str,
    project_dict: dict,
    mr_access_token: str,
    mr_base_url: str,
    verify: bool=True
):
    json_data = dumps(project_dict)
    url = mr_base_url + '/api/projects/update/'
    print(project_id)
    rest_response = requests.post(
        url,
        headers= {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Token': mr_access_token,
            },
        data=json_data,
        params={'project': project_id},
        verify=verify
    )
    return rest_response

def add_element(project_dict:dict, section_name:str, new_element_dict:dict):
    section_elements = project_dict.pop(section_name)
    new_element_id = new_element_dict['id']
    assert new_element_id not in section_elements
    section_elements[new_element_id] = new_element_dict
    project_dict[section_name] = section_elements
    # validate_json(project_dict) Output from /api/projects/json does not currently validate
    return project_dict, new_element_id

def add_tree_fn(project_id, newick, mr_access_token, mr_base_url, verify):
    rest_response = get_project_json_fn(
        project_id=project_id,
        mr_access_token=mr_access_token,
        mr_base_url=mr_base_url,
        verify=verify
    )
    project_dict = rest_response.json()

    """We have to add something to both the files section and the trees section.
    The newick data will go into the files section."""

    # files section
    new_file_dict = classes.File(type='tree', body=newick).to_dict()
    project_dict, new_file_id = add_element(project_dict, 'files', new_file_dict)

    # trees section
    new_tree_dict = classes.Tree(file=new_file_id).to_dict()
    project_dict, _new_tree_id = add_element(project_dict, 'trees', new_tree_dict)

    rest_response = update_project_fn(
        project_id=project_id,
        project_dict=project_dict,
        mr_access_token=mr_access_token,
        mr_base_url=mr_base_url,
        verify = verify
        )

    return rest_response