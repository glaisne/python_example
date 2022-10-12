import json
import az
from azure.identity import AzureCliCredential

config_file_path = "./testing_config.json"

# import base json configuration file
with open(config_file_path, "r") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()


#todo: Working here. getting everything together ot create a resoruce group and try testing it.

# <not ready yet> az.create_resource_group(credential, config)
