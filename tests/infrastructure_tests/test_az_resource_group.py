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



@pytest.fixture
def config():
    CONFIG_FILE_PATH = "./testing_config.json"

    # import base json configuration file
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
        config_data = config_base.read()
        
    return json.loads(config_data)

# Acquire a credential object using CLI-based authentication.
@pytest.fixture
def credential():
    return AzureCliCredential()

# Obtain the management object for resources.
@pytest.fixture
def client():
    return ResourceManagementClient(credential, config['subscription_id'])

def test_resource_group_name(client, config):
    '''Test that the resource group exists and has the proper name'''
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg != None

def test_resource_group_location(client, config):
    '''Test that the resource group is in the correct location'''
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg.location == config['resource_group']['locaiton']
