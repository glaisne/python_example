'''
Tests for all resource group functions in the azure module
'''

import json
import os
import sys
import pytest
from azure.identity import AzureCliCredential

# Adds the parent directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import the azure module from the parent directory
from context import az

@pytest.fixture(name="credential")
def setup_credential():
    '''pytest fixture for cli credentials'''
    return AzureCliCredential()

@pytest.fixture(name="subscription_id")
def setup_subscription_id():
    '''pytest fixture for cli subscrption_id'''
    return '00000000-0000-0000-0000-000000000000'

@pytest.fixture(name="config_good")
def setup_good_config():
    '''Read the existing config file and make it good.'''
    CONFIG_FILE_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), '../../config/config_az_OPSTESTING.json'))

    # import base json configuration file
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
        config_data = config_base.read()

    # do string replacement.
    config_data = config_data.replace('<environment>', 'opstesting')

    config = json.loads(config_data)
    if isinstance(config['resource_group'], dict):
        return config['resource_group']
    else:
        return config['resource_group'][0]



@pytest.fixture(name="config_bad_name")
def setup_config_with_bad_resource_group_name(config_good):
    '''take a valid configuration and modify the resource group name to be bad'''
    tmpconfig = config_good
    tmpconfig['name'] = 'bad|name.'
    return tmpconfig

@pytest.fixture(name="config_bad_location")
def setup_config_with_bad_location(config_good):
    '''take a valid configiruation and swap out a bad location'''
    tmpconfig = config_good
    tmpconfig['location'] = 'bad_location'
    return tmpconfig






def test_create_rg_bad_rg_name(credential, subscription_id, config_bad_name):
    '''pytest to validate the proper raise occurse with an invalid resource group name'''
    with pytest.raises(ValueError, match=' is NOT a valid resource group name'):
        az.create_resource_group(credential, subscription_id, config_bad_name)

def test_create_rg_bad_location(credential, subscription_id, config_bad_location):
    '''pytest to validate the proper raise occurse with an invalid locaiton'''
    with pytest.raises(ValueError, match=' is NOT a valid location'):
        az.create_resource_group(credential, subscription_id, config_bad_location)
