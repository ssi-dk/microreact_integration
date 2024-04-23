# README for the microreact_integration package

## Environment variables

microreact_integration will need these environment variables to be set:

- MICROREACT_BASE_URL: Base URL where Microreact is available
- MICROREACT_ACCESS_TOKEN = Personal access token for a Microreact user

## Command-line scripts

Although microreact_integration is primarily intended to use as a library for installing in other Ptyhon projects it has a few command-line scripts that can be used directly.

### get_project

This script will get all information stored in MongoDB from an existing Microreact project. It will NOT return any actual data values from (like sequence ID's metadata content, etc.) since Microreact
stores the actual data values on a filesystem that normally is unavailable fro users. The information that get_project will fetch is data about the project structure and layout.

usage:

    python get_project.py <project id> --noverify

--noverify is an optional argument that will skip SSL certificate checking.

Only projects that are owned by the Microreact user who owns MICROREACT_ACCESS_TOKEN can be fetched.

### new_project

Todo.

### add_tree

Todo.
