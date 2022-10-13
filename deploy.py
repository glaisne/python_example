import az
import getopt
import json
import sys
from azure.identity import AzureCliCredential

CONFIG_FILE_PATH = "./testing_config.json"

# import base json configuration file
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_base:
    config_data = config_base.read()

config = json.loads(config_data)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

try:
    opts, args = getopt.getopt(sys.argv[1:],"hc:",["CONFIG_FILE_PATH="])
except getopt.GetoptError:
    print('build_data.py -c <CONFIG_FILE_PATH>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('build_data.py -c <CONFIG_FILE_PATH>')
        sys.exit()
    elif opt in ("-c", "--CONFIG_FILE_PATH"):
        CONFIG_FILE_PATH = arg


#todo: Working here. getting everything together ot create a resoruce group and try testing it.

# <not ready yet> az.create_resource_group(credential, config)
