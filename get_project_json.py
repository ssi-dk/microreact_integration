import argparse
from json import dumps

import common
from functions import get_project_json

parser = argparse.ArgumentParser()
parser.add_argument("project_id", help="The unique ID that defines the Microreact project")
parser.add_argument(
    "--noverify",
    help="Do not verify SSL certificate of Microreact host ",
    action="store_true"
    )
args = parser.parse_args()

rest_response = get_project_json(
    project_id=args.project_id,
    mr_access_token=common.MICROREACT_ACCESS_TOKEN,
    mr_base_url=common.MICROREACT_BASE_URL,
    verify = not args.noverify
    )
print(f"HTTP response code: {str(rest_response)}")
print("Response as actual JSON:")
print(dumps(rest_response.json()))