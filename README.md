# README for the Microreact Integration package

## Functions in functions.py

These are the main functions meant for external use in functions.py:

- new_project
- get_project_json
- update_project

In order to use the functions, these prerequisites have to be fulfilled:

- A running instance of Microreact which can be accessed with http(s) from the location where Python is running
- An personal access token that will permit creation of projects in Microreact for a user

When a user is logged into Microreact, his/her access token will be visible at <https://MICROREACT_BASE:URL/my-account/settings>.
The calling system should have a stored copy of this token for each user.

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

The name of the project as it will appear in Microreact. The project owner can later change the name from inside Microreact.

#### tree_calcs

A list of dicts (or dict-like objects like MongoDB documents) which represent the trees that should be exported to Microreact.

The dicts must contain these keys:

- method: str - this string will be used as name for the tree in Microreact
- result: str - this is the actual tree structure formatted in Newick format

#### metadata_keys

This is a list of str elements that will be used as column names in the data table in Microreact.

#### metadata_values

This should be a list of lists where each element in the outer list represents a column in the data table and the elements in each inner list
hold the actual data for that column.

#### mr_access_token

The access token for the users who will own the project in Microreact.

#### mr_base_url

The base URL for the Microreact instance.

#### public

Optional Booelan. If set to True, the created Microreact project will be public. Default is False.

#### verify

Optional Boolean. If set to False, it will not be checked if the Microreact instance has a valid SSL certificate. Default is True.
