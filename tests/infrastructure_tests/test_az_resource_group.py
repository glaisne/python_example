'''
Testing resource groups created by the az module
'''
import os
import sys
import json
from azure.identity import AzureCliCredential

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

print(credential)
# todo - Working here. getting everything together ot create a resoruce group and try testing it.

# <not ready yet> az.create_resource_group(credential, config)

def test_valid_guid():
    '''test that a valid guid returns 1'''
    assert az.validate_guid('670196b2-4db2-4cb2-a792-088bcfb4efc1') == 1
