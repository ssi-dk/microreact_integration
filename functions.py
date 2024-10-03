from json import dumps, dump, load
import requests
from typing import Optional

from . import classes

def stringify(value_list):
    line = ";".join([str(value) for value in value_list])
    return line + "\n"


def build_basic_project_dict(
        project_name: str,
        metadata_keys: list,
        metadata_values: list,
        tree_calcs: list,
        raw_matrices: list=list(),
        hidden: list=list()):
    """
    Create a Microreact project where the metadata table is constructed from lists of keys and values.

    project_name: the name that will be shown for the project
    metadata_keys: keys of the metadata fields as a list. The first one will become the id field
    metadata_values: metadata values as a list of lists
    trees: list with trees in Newick format (as strings)

    Returns: a dict structure that is validated with MR's JSON schema and can be converted to JSON with json.dumps().
    """
    project_meta = classes.Meta(name=project_name)
    id_field_name = metadata_keys[0]

    metadata_body = str()
    metadata_body += stringify(metadata_keys)  # Add keys as first line in body
    for record in metadata_values:
        metadata_body += stringify(record)

    metadata_file = classes.File(type='data', body=metadata_body)
    dataset = classes.Dataset(file=metadata_file.id, idFieldName=id_field_name)

    files = [metadata_file]
    trees = list()
    tree_number = 1
    for tree_calc in tree_calcs:
        newick_file = classes.File(type='tree', body=tree_calc['result'])
        files.append(newick_file)
        tree =  classes.Tree(
                type='rc',
                title=tree_calc['method'],
                labelField=id_field_name,
                file=newick_file.id,
                highlightedId=None
            )
        trees.append(tree)
        tree_number += 1

    table = classes.Table(title='Metadata', columns=metadata_keys, file=metadata_file.id, hidden=hidden, dataset=dataset)

    matrices = list()
    matrix_idx = 0
    for raw_matrix in raw_matrices:
        matrix_idx += 1
        matrix_file = classes.File(type='data', body=raw_matrix, name="matrix_" + str(matrix_idx))
        files.append(matrix_file)
        matrix=classes.Matrix(file=matrix_file, title="Matrix " + str(matrix_idx))
        #matrices.append(matrix)

    project = classes.Project(
        meta=project_meta,
        datasets=[dataset],
        files=files,
        tables=[table],
        trees=trees,
        matrices=matrices
    )

    return project.to_dict()

def build_basic_project_dict_2(
        project_name: str,
        metadata_url: str,
        columns: list,
        tree_calcs: list,
        raw_matrix: str=None,
        hidden: list=list()
        ):
    """
    Create a Microreact project where the metadata table is defined using an external URL.
    
    project_name: the name that will be shown for the project
    metadata_url: url containing af metadatalist. The first column will become the id field
    columns: list of columns to read from metadata_url. Only these column will exist in the Microreact project,
    and per default all columns will be visible.
    tree_calcs: list with trees in Newick format (as strings)
    hidden: an optional list of columns to be marked and hidden in the Microreact project.

    Returns: a dict structure that is validated with MR's JSON schema and can be converted to JSON with json.dumps().
    """
    project_meta = classes.Meta(name=project_name)
    id_field_name = columns[0]

    metadata_file = classes.File(type='data', url=metadata_url)
    dataset = classes.Dataset(file=metadata_file.id, idFieldName=id_field_name)

    files = [metadata_file]
    trees = list()
    tree_number = 1
    for tree_calc in tree_calcs:
        newick_file = classes.File(type='tree', body=tree_calc['result'])
        files.append(newick_file)
        tree =  classes.Tree(
                type='rc',
                title=tree_calc['method'],
                labelField=id_field_name,
                file=newick_file.id,
                highlightedId=None
            )
        trees.append(tree)
        tree_number += 1

    table = classes.Table(title='Metadata',
                          columns=columns,
                          file=metadata_file.id,
                          dataset=dataset.id,
                          hidden=hidden
                          )

    project = classes.Project(
        meta=project_meta,
        datasets=[dataset],
        files=files,
        tables=[table],
        trees=trees
    )

    return project.to_dict()

def new_project(
    project_name: str,
    tree_calcs: list,
    metadata_keys: list,
    metadata_values: list,
    mr_access_token: str,
    mr_base_url: str,
    raw_matrices: list[str] = list(),
    public: bool=False,
    hidden:list = list(),
    verify: bool=True
):
    project_dict = build_basic_project_dict(project_name, metadata_keys, metadata_values, tree_calcs,
                                                raw_matrices=raw_matrices)
    print(project_dict)
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

def new_project_2(
    project_name: str,
    metadata_url: str,
    columns: list,
    mr_access_token: str,
    mr_base_url: str,
    tree_calcs: list = list(),
    hidden:list = list(),
    public: bool=False,
    verify: bool=True
):
    print(f"Metadata URL: {metadata_url}")
    project_dict = build_basic_project_dict_2(project_name, metadata_url, columns, tree_calcs, hidden)
    json_data = dumps(project_dict, indent=4)
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

def new_project_file(
    project_name: str,
    tree_calcs: list,
    metadata_keys: list,
    metadata_values: list,
    file_name: str
):
    project_dict = build_basic_project_dict(project_name, metadata_keys, metadata_values, tree_calcs)
    with open(file_name , "w") as f:
        dump(project_dict, f)
    print(f"Saved {file_name}")

def get_project_json(
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

def update_project(
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
    rest_response = get_project_json(
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

    rest_response = update_project(
        project_id=project_id,
        project_dict=project_dict,
        mr_access_token=mr_access_token,
        mr_base_url=mr_base_url,
        verify = verify
        )

    return rest_response