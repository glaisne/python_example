###################################################################
#  Purpose:
#    This scirpt will import a jason file which has pre-configured
#    information needed about the environment. To that, the script
#    will MODIFY values based on the current implementation.
#
#  Notes:
#    - I tried using purely JSON calls (import, modify, write), 
#      but the JSON lookup for keys was case sensitive. In this
#      version, I have the ability to manage case sensitivity. it
#      is more work, but it does work.
#
#  future improvements:
#    - Add the ability to ADD a value as opposed to just overwrite
#      existing values.
###################################################################

import json, re, getopt, sys, pprint

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:f:",["subscription_id=", "file_path="])
except getopt.GetoptError:
    print('update_config_file.py -s <subscription_id> -f <file_path>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('update_config_file.py -s <subscription_id> -f <file_path>')
        sys.exit()
    elif opt in ("-s", "--subscription_id"):
        subscription_id = arg
    elif opt in ("-f", "--file_path"):
        file_path = arg


def process_json(json_as_string):

    result = re.findall(r"<[\w_-]+>", json_as_string)

    # if there was nothing, return the original
    if (result == None):
        return json_as_string

    jsontmp = json.loads(json_as_string)
    swaps = {}
    return_json = json_as_string

    # get all the replacements
    for match in result:
        #if match in Vehicles:
        if (not match in swaps.keys()):
            # get the base variable name
            variable = match.lstrip('<')
            variable = variable.rstrip('>')
            if (jsontmp[variable] != None):
                swaps[match] = jsontmp[variable]

    # make all the swaps
    for swap in swaps:
        return_json = return_json.replace(swap, swaps[swap])
    
    # return the result
    return return_json


# create the dictionary of passed in values that will be replaced or added to the json
overwriters = {}

if (subscription_id):
    overwriters["subscription_id"] = subscription_id

# import base json configuration file
with open(file_path, "r") as config_base:
    config = config_base.read()

#print(config)

# overwrite fields from input
for replacement in overwriters:
    compiled_regex = re.compile(r'\n\s*"{}"\s*\:\s*"[a-z0-9\.-_]+"\s*,\s*'.format(replacement.upper()), re.IGNORECASE)

    matches = compiled_regex.findall(config)
    if (isinstance(matches, list)):
        for match in matches:
            value_find_regex = re.compile(r'\n\s*"{}"\s*\:\s*"(?P<value>[a-z0-9\.-_]+)"\s*,\s*'.format(replacement.upper()), re.IGNORECASE)
            to_replace = value_find_regex.search(match)
            config = config.replace(to_replace.group('value'), overwriters[replacement])
    else: 
        pprint.pprint(matches)

# Find replacement strings and replace them.
config = process_json(config)
config = process_json(config)

# Write back to disk the updated json file
with open(file_path, "w") as output:
    output.write(config)