'''
Testing resource groups created by the az module
'''
# import os         # needed if az is used at some later date
# import sys        # needed if az is used at some later date
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

# # Adds the parent directory to the module search path
# needed if az is used at some later date
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # import the azure module from the parent directory
# needed if az is used at some later date
# from context import az



@pytest.fixture(name='config')
def setup_config():
    '''load the json config file'''
    config_file_path = "./config/config_az_OPSTESTING.json"

    # import base json configuration file
    with open(config_file_path, "r", encoding="utf-8") as config_base:
        config_data = config_base.read()

    return json.loads(config_data)


# Obtain the management object for resources.
@pytest.fixture(name='client')
def setup_client(config):
    '''setup the Azure ResourceManagmentClient'''
    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()

    return_client =  ResourceManagementClient(credential, config['subscription_id'])
    return return_client


def test_resource_group_name(client, config):
    '''Test that the resource group exists and has the proper name'''
    resource_group = client.resource_groups.get(config['resource_group']['name'])
    assert resource_group is not None

def test_resource_group_with_bad_name(client):
    '''Test that an incorrect given name does not exist'''
    resource_group_name = 'aksdhfoasndfkazsehfzsawsjs03885252'
    with pytest.raises(ResourceNotFoundError, match=f"Resource group '{resource_group_name}' could not be found"):
        client.resource_groups.get('aksdhfoasndfkazsehfzsawsjs03885252')


def test_resource_group_location(client, config):
    '''Test that the resource group is in the correct location'''
    resource_group = client.resource_groups.get(config['resource_group']['name'])
    assert resource_group.location == config['resource_group']['location']

def test_resource_group_is_not_in_a_different_location(client, config):
    '''Test that the resource group is not in an incorrect location'''
    resource_group = client.resource_groups.get(config['resource_group']['name'])
    assert resource_group.location != 'norwaywest'
