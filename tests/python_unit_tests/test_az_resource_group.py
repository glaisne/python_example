'''
Tests for all resource group functions in the azure module
'''

import json
import os
import pytest
import sys
from azure.identity import AzureCliCredential

# Adds the parent directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import the azure module from the parent directory
from context import az

CONFIG_FILE_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), '../../testing_config.json'))

# import base json configuration file
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

@pytest.fixture
def credential():
    return AzureCliCredential()

@pytest.fixture
def good_config():
    config['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return config

@pytest.fixture
def config_with_bad_resource_group_name():
    tmpconfig = config
    tmpconfig['resource_group']['name'] = 'bad|name.'
    tmpconfig['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return tmpconfig

@pytest.fixture
def config_with_bad_location():
    tmpconfig = config
    tmpconfig['resource_group']['location'] = 'bad_location'
    tmpconfig['subscription_id'] = '00000000-0000-0000-0000-000000000000'
    return tmpconfig


#def create_rg_bad_rg_name(credential, good_config):

def test_create_rg_bad_rg_name(credential, config_with_bad_resource_group_name):
    with pytest.raises(ValueError, match=' is NOT a valid resource group name'):
        az.create_resource_group(credential, config_with_bad_resource_group_name)

def test_create_rg_bad_location(credential, config_with_bad_location):
    with pytest.raises(ValueError, match=' is NOT a valid location'):
        az.create_resource_group(credential, config_with_bad_location)