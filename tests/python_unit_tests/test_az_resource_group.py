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

CONFIG_FILE_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), '../../config_az.json'))

# import base json configuration file
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

@pytest.fixture
def credential():
    '''pytest fixture for cli credentials'''
    return AzureCliCredential()

@pytest.fixture
def good_config():
    '''Take a valid configuration and add a generic guid subscription_id'''
    tmpconfig = json.loads(config_data)
    tmpconfig['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return tmpconfig

@pytest.fixture
def config_with_bad_resource_group_name():
    '''take a valid configuration and modify the resource group name to be bad'''
    tmpconfig = json.loads(config_data)
    tmpconfig['resource_group']['name'] = 'bad|name.'
    tmpconfig['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return tmpconfig

@pytest.fixture
def config_with_bad_location():
    '''take a valid configiruation and swap out a bad location'''
    tmpconfig = json.loads(config_data)
    tmpconfig['resource_group']['location'] = 'bad_location'
    tmpconfig['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return tmpconfig


#def create_rg_bad_rg_name(credential, good_config):

def test_create_rg_bad_rg_name(credential, config_with_bad_resource_group_name):
    '''pytest to validate the proper raise occurse with an invalid resource group name'''
    with pytest.raises(ValueError, match=' is NOT a valid resource group name'):
        az.create_resource_group(credential, config_with_bad_resource_group_name)

def test_create_rg_bad_location(credential, config_with_bad_location):
    '''pytest to validate the proper raise occurse with an invalid locaiton'''
    with pytest.raises(ValueError, match=' is NOT a valid location'):
        az.create_resource_group(credential, config_with_bad_location)
