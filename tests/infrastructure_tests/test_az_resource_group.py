'''
Testing resource groups created by the az module
'''
import os
import sys
import json
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

# Adds the parent directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import the azure module from the parent directory
from context import az

CONFIG_FILE_PATH = "./testing_config.json"

# import base json configuration file
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential,
                    config['subscription_id'])

def test_resource_group_name(client, config):
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg != None