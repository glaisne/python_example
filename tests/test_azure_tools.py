'''
Tests for all the "tools" functions in the azure module
'''

# import the azure module from the parent directory
from .context import az

def test_valid_guid():
    '''test that a valid guid returns 1'''
    assert az.validate_guid('670196b2-4db2-4cb2-a792-088bcfb4efc1') == 1

def test_invalid_guid():
    '''test that an invalid guid returns 0'''
    assert az.validate_guid('670196b2-4db2-4cb2-a792-088bcfb4efc') == 0

def test_validate_rg_name():
    '''test a valid resource group name'''
    assert az.validate_resource_group_name('thisisavalidrgname') = 1

def test_bad_rg_name01():
    '''
    test a valid resource group name
    It is invalid becasue there is an '_'
    '''
    assert az.validate_resource_group_name('this_isainvalidrgname') = 0

def test_bad_rg_name02():
    '''
    test a valid resource group name
    It is invalid becasue there is a capital letter
    '''
    assert az.validate_resource_group_name('Thisisainvalidrgname') = 0

def test_bad_rg_name03():
    '''
    test a valid resource group name
    It is invalid becasue it is too long
    '''
    assert az.validate_resource_group_name('thisisavalidresourcegroupname') = 0