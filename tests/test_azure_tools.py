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
