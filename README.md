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

The function takes these arguments:

    - project_name: str,
    - tree_calcs: list,
    - metadata_keys: list,
    - metadata_values: list,
    - mr_access_token: str,
    - mr_base_url: str,
    - public: bool=False,
    - verify: bool=True
