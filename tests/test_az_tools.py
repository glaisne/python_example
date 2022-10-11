'''
Tests for all the "tools" functions in the azure module
'''

# import the azure module from the parent directory
from .context import az

# guid tests

def test_valid_guid():
    '''test that a valid guid returns 1'''
    assert az.validate_guid('670196b2-4db2-4cb2-a792-088bcfb4efc1') == 1

def test_invalid_guid():
    '''
    test that an invalid guid returns 0
    It is invalid because there are too few characters
    '''
    assert az.validate_guid('670196b2-4db2-4cb2-a792-088bcfb4efc') == 0

# resource group name tests

def test_validate_rg_name():
    '''test a valid resource group name'''
    assert az.validate_resource_group_name('thisisavalidrgname') == 1

def test_bad_rg_name01():
    '''
    test a invalid resource group name
    It is invalid becasue there is a '.' at the end
    '''
    assert az.validate_resource_group_name('thisisaninvalidresourcegroupname.') == 0

def test_bad_rg_name02():
    '''
    test a invalid resource group name
    It is invalid becasue there is a '|'
    '''
    assert az.validate_resource_group_name('thisisaninvalid|resourcegroupname') == 0

def test_bad_rg_name03():
    '''
    test a invalid resource group name
    It is invalid becasue there is a '/'
    '''
    assert az.validate_resource_group_name('thisisaninvalid/resourcegroupname') == 0

# location tests

def test_valid_location():
    '''test a valid entry in the list of locations'''
    assert az.validate_location('eastus') == 1

def test_invalid_location_01():
    '''
    test an invalid location name
    It is invalid because it is a random set of characters
    '''
    assert az.validate_location('asdfasnfwjdfsh') == 0

# storage account name tests

def test_valid_storage_account_name():
    '''test a valid storage account name'''
    assert az.validate_storage_account_name('this-is-1-valid-name') == 1

def test_invalid_storage_account_name_01():
    '''
    test an invalid storage account name
    It is invalid because it has too characters (25)
    '''
    assert az.validate_storage_account_name('this-is-1-invalid-namexxx') == 0

def test_invalid_storage_account_name_01():
    '''
    test an invalid storage account name
    It is invalid because it has a '_'
    '''
    assert az.validate_storage_account_name('this_is-1-invalid-name') == 0