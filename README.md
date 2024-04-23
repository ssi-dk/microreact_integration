# README for the microreact_integration package

## Environment variables

microreact_integration will need these environment variables to be set:

- MICROREACT_BASE_URL: Base URL where Microreact is available
- MICROREACT_ACCESS_TOKEN = Personal access token for a Microreact user

## Command-line scripts

Although microreact_integration is primarily intended to use as a library for installing in other Python projects it has a few command-line scripts that can be used directly.

The scripts are intended for testing and demo purposes only.

All scripts take an optional --noverify argument. If this is provided the script will skip checking SSL certificate validity.

### get_project

This script will print all information stored in MongoDB for an existing Microreact project owned by the Microreact user given by MICROREACT_ACCESS_TOKEN. It will NOT fetch any actual data values (like sequence ID's, metadata content, etc.) since Microreact
stores these on a filesystem that normally is unavailable for users. The information that get_project will fetch is data about the project structure and graphical layout.

usage:

    python get_project.py <project_id> <--noverify>

*project_id*: The unique ID which defines the project.

Only projects that are owned by the Microreact user who owns MICROREACT_ACCESS_TOKEN can be fetched.

### new_project

This script will create a new project that will be owned by the user given by MICROREACT_ACCESS_TOKEN. The project will we a minimal project and will only contain a tree.

Usage:

    python new_project.py <project_id> <newick_file>

*project_id*: The unique ID that will define the project.
*newick_file*:  Path to a Newick file containing the tree to add

### add_tree

This script will add another tree to an existing project owned by the user given by MICROREACT_ACCESS_TOKEN.

Usage:

    python add_tree.py <project_id> <newick_file>

*project_id*: The unique ID that defines the project.
*newick_file*:  Path to a Newick file containing the tree to add
