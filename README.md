# README for the microreact_integration package

## Functions in functions.py

These are the main functions meant for external use in functions.py:

- new_project
- get_project_json
- update_project

In order to use the functions, these prerequisites have to be made:

- A running instance of Microreact which can be accessed with http(s) from the location where Python is running
- An access token that will permit creation of projects in Microreact

### new_project

Mandatory arguments:

    - project_name: str
    - tree_calcs: list
    - metadata_keys: list
    - metadata_values: list
    - mr_access_token: str
    - mr_base_url: str

Optional arguments:

    - public: bool=False
    - verify: bool=True

#### project_name

The name of the project as it will appear in Microreact. The project owner can later change the name from insiside Microreact.

#### tree_calcs

A list of dicts (or dict-like objects like MongoDB documents) which represent the trees that should be exported to Microreact.

The dicts must contain these keys:

- method: str - this string will be used as title for the tree Microreact
- result: str - this is the actual tree structure formatted in Newick format