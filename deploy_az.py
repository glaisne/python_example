import az
import getopt
import json
import sys
from azure.identity import AzureCliCredential


try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:c:",["SUBSCRIPTION_ID=", "CONFIG_FILE_PATH="])
except getopt.GetoptError:
    print('update_config_file.py -s <SUBSCRIPTION_ID> -c <CONFIG_FILE_PATH>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('update_config_file.py -s <SUBSCRIPTION_ID> -c <CONFIG_FILE_PATH>')
        sys.exit()
    elif opt in ("-c", "--CONFIG_FILE_PATH"):
        CONFIG_FILE_PATH = arg
    elif opt in ("-s", "--SUBSCRIPTION_ID"):
        SUBSCRIPTION_ID = arg

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# import base json configuration file
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

# deploy resoruce group(s)
if isinstance(config['resource_group'], dict):
    az.create_resource_group(credential, SUBSCRIPTION_ID, config['resource_group'])
else:
    for rg_config in config['resource_group']:
        az.create_resource_group(credential, SUBSCRIPTION_ID, rg_config)

