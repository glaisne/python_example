'''
Module for working with Azure SDK
'''

###############################################################################
#
#    Imports
#
###############################################################################

import re
from azure.mgmt.resource import ResourceManagementClient

###############################################################################
#
#    Tools
#
###############################################################################


def validate_guid(guid):
    '''
    validates a string as being a proper guid

    parameter:
    guid (string): a string to test if it is a proper guid

    Returns:
    (int) 1 if the string is a proper guid
    (int) 0 if the string is not a proper guid
    '''

    regex = r"^[{(]?[0-9A-F]{8}[-]?([0-9A-F]{4}[-]?){3}[0-9A-F]{12}[)}]?$"

    if re.match(regex, guid, flags=re.IGNORECASE):
        return 1
    else:
        return 0

def validate_resource_group_name(resource_group_name):
    '''
    validates a string as being a valid resource group name

    parameter:
    resource_group_name (string): a string to test if it is a valid resource group name

    Returns:
    (int) 1 if the string is a valid resource group name
    (int) 0 if the string is not a valid resource group name
    '''
    regex = r"^[-\w\._\(\)]+$"

    if re.match(regex, resource_group_name, flags=re.IGNORECASE):
        # Also check for ending with a '.'
        # from https://learn.microsoft.com/en-us/rest/api/resources/resource-groups/create-or-update
        # The name of the resource group to create or update. 
        # Can include alphanumeric, underscore, parentheses, 
        # hyphen, period (except at end), and Unicode characters 
        # that match the allowed characters.
        if re.match(r".*\.$", resource_group_name):
            print('first 0')
            return 0
        else:
            print('first 1')
            return 1
    else:
        print('second 0')
        return 0
        

def validate_location(location):
    '''
    validates a string as being a valid azure datacenter location

    parameter:
    resource_group_name (string): a string to test if it is a valid azure datacenter location

    Returns:
    (int) 1 if the string is a valid azure datacenter location
    (int) 0 if the string is not a valid azure datacenter location
    '''
    location_list = ['eastus', 'eastus2', 'southcentralus', 'westus2',
                      'westus3', 'australiaeast', 'southeastasia',
                      'northeurope', 'swedencentral', 'uksouth', 'westeurope',
                      'centralus', 'southafricanorth', 'centralindia',
                      'eastasia', 'japaneast', 'koreacentral',
                      'canadacentral', 'francecentral', 'germanywestcentral',
                      'norwayeast', 'switzerlandnorth', 'uaenorth',
                      'brazilsouth', 'eastus2euap', 'qatarcentral', 'asia',
                      'asiapacific', 'australia', 'brazil', 'canada',
                      'europe', 'france', 'germany', 'global', 'india',
                      'japan', 'korea', 'norway', 'southafrica',
                      'switzerland', 'unitedstates', 'northcentralus',
                      'westus', 'centraluseuap', 'westcentralus',
                      'southafricawest', 'australiacentral',
                      'australiacentral2', 'australiasoutheast', 'japanwest',
                      'koreasouth', 'southindia', 'westindia', 'canadaeast',
                      'francesouth', 'germanynorth', 'norwaywest',
                      'switzerlandwest', 'ukwest', 'uaecentral',
                      'brazilsoutheast']

    if location in location_list:
        return 1
    else:
        return 0


def validate_storage_account_name(storage_account_name):
    '''
    validates a string as being a valid storage account name

    parameter:
    resource_group_name (string): a string to test if it is a valid storage account name

    Returns:
    (int) 1 if the string is a valid storage account name
    (int) 0 if the string is not a valid storage account name
    '''
    regex = r"^[a-z0-9-]{3,24}$"

    if re.match(regex, storage_account_name, flags=re.IGNORECASE):
        return 1
    else:
        return 0




###############################################################################
#
#    Resource Groups
#
###############################################################################



def create_resource_group(credential, config):
    '''
    Create a resource group with the given name in the given locaiton

    parameter:
    resoruce_group_name (string): name of the resoruce group to be created
    location (string): name of the location the resource group should be created in

    Returns:
    (string) <json>: Json information about the resoruce group that was created
    
    Exceptions:
    ValueError
    httpresponseerror - https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions.httpresponseerror?view=azure-python
    '''
    # validate parameters
    if not validate_guid(config['subscription_id']):
        raise ValueError(f"'{config['subscription_id']}' is NOT a valid"
                          " guid.")
    if not validate_resource_group_name(
                config['resource_group']['name']):
        raise ValueError(f"'{config['resource_group']['name']}' is NOT a valid"
                          " resource group name.")
    if not validate_location(config['location']):
        raise ValueError(f"'{config['location']}' is NOT a valid location.")

    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential,
                      config['subscription_id'])

    # Provision the resource group.
    return resource_client.resource_groups.create_or_update(
        config['resource_group']['name'],
        {
            'location': config['resource_group']['location']
        }
    )
