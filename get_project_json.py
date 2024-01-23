import argparse
from pathlib import Path

import env
from functions import get_project_json_fn

parser = argparse.ArgumentParser()
parser.add_argument("project_id", help="The unique ID that defines the Microreact project")
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

rest_response = get_project_json_fn(
    project_id=args.project_id,
    mr_access_token=env.MICROREACT_ACCESS_TOKEN,
    mr_base_url=env.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"REST response: {str(rest_response)}")
print(rest_response.json())