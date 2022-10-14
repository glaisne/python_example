'''
Testing resource groups created by the az module
'''
import os
import sys
import json
import pytest
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import (
#    ClientAuthenticationError,
#    HttpResponseError,
#    ServiceRequestError,
    ResourceNotFoundError,
#    AzureError
)

# Adds the parent directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import the azure module from the parent directory
from context import az



@pytest.fixture
def config():
    CONFIG_FILE_PATH = "./config_az.json"

    # import base json configuration file
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
        config_data = config_base.read()

    return json.loads(config_data)


# Obtain the management object for resources.
@pytest.fixture
def client(config):
    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()

    return_client =  ResourceManagementClient(credential, config['subscription_id'])
    return return_client


def test_resource_group_name(client, config):
    '''Test that the resource group exists and has the proper name'''
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg != None

def test_resource_group_with_bad_name(client, config):
    '''Test that an incorrect given name does not exist'''
    resource_group_name = 'aksdhfoasndfkazsehfzsawsjs03885252'
    with pytest.raises(ResourceNotFoundError, match=f"Resource group '{resource_group_name}' could not be found"):
        client.resource_groups.get('aksdhfoasndfkazsehfzsawsjs03885252')


def test_resource_group_location(client, config):
    '''Test that the resource group is in the correct location'''
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg.location == config['resource_group']['location']

def test_resource_group_is_not_in_a_different_location(client, config):
    '''Test that the resource group is not in an incorrect location'''
    rg = client.resource_groups.get(config['resource_group']['name'])
    assert rg.location != 'norwaywest'
