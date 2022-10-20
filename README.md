# PYTHON_EXAMPLE
Testing a Jenkins environment with Python script to Azure using pylint and pytest. Additionally, the project is built around the idea that in the future, other clouds would be added to the functionality.

# FILES AND FOLDERS
* ``./requirements.txt`` - List of modules required by this project to be called by pip for installation
* ``./jenkinsfile-(dev|test|stage|prod)`` - These are the jenkins files used for "real" environments. For all of these, it is assumed this deploy is a new environment.
* ``./jenksinsfile-OpsTesting`` - This jenkins file is a special. This includes linting (pylint), python unit tests (pytest) and infrastructer tests (pytest). These would be extra steps to ensure the code is good for any given deployment before the code is moved to dev, test, stage, or prod.
* ``./pylint_confi``g`` - Configuration file for lint testing (See: Setup/pylint below)
* ``./pylint_config_local`` - Configuration file for lint testing when used for local testing
   * Note: ```*_local``` in ``.gitignore``
* ``./az.py`` - Module of Azure classes and functions used for this project. 
   * In the future, it is assumed there would be an aws.py and/or gcp.py or other modules for other clouds.
* ``./deploy_az.py`` - This script leverages the classes and functions in az.py for deploying infrastructre to Azure.
   * In the future, it is assumed there would be an deploy_aws.py and/or deploy_gcp.py or other modules for other clouds.
* ``./tests`` - Folder for all files related to testing
* ``./tests/context.py`` - Used for importing root folder modules (./az.py in this example)
* ``./tests/infrastructure_tests`` - files for infrastructer-specifc tests (ex: did the resource get created correctly)
* ``./tests/infrastructure_tests/test_az_resource_group.py`` - pytest script file used to evaluate the resoruce group created as part of the (in this case) deploy_az.py script.
* ``./tests/python_unit_tests`` - directory of unit tests specifically for the Cloud Module (``az.py``)
* ``./tests/python_unit_tests/__init__.py`` - for some reason, this file is needed. pytests won't work without it. it is empty.
* ``./tests/python_unit_tests/test_az_resource_group.py`` - pytest script for testing azure resource group specific code in the az.py module file.
* ``./tests/python_unit_tests/test_az_tools.py`` - pytest script for testing azure tools specific code in the az.py module file.

# SETUP
## .gitignore
In some cases, you may want to test with local configurations that are different than on the jenkins system. For those configurations, I added ```*_local``` to the gitignore.

## pylint
configuration file created from this call:
```cmd
pylint --disable=no-else-return,trailing-whitespace --generate-rcfile --max-line-length 140 > pylint.config2
```
Then the file was paired down to just the parts that were configured, leaving the rest of it configured to use
the defaults.

# jenskinsfile-* NOTES
## Goal
All information flows from the jenkins file. In other words if a script requires some piece of information to run, its origin should be found in the jenkins file. For example, the CLOUD_CODE, SUBSCRIPTION_ID and ENVIRONMENT are required by various scripts later on (infrastructre tests, deployment script...) that information is passed to those script files via parameter and the original value comes from jenkins.


## Setup 'stage'
Everything for setup going forward should happen at this step:
* Installing any neeeded python modules
* Modifying any configuration files (Of course any updated configuration file should be sent to output)
* Copying/moving/creating any files used as a source of data should be done here.

## Informaiton 'stage'
Any information, not already displayed, should be displayed here.

Other stages should be self-explanitory

# pytest
## how it works (here)
It is worth understanding how the pytest scripts work in this layout. I wanted to separate unit tests with infrastructre tests. The easiest way to do that is to split them out by folder paths. To do that, we need some extra work to be done to load the Cloud Module file (in this case az.py).

The pytest script is called from the jenkins file for either unit tests or infrastructure tests by specifying the directory with those test in it (Note that for the infrastructer tests we use the -k switch which includes only those files which match the given string '_${CLOUD_CODE}_' - This ensures we only run the tests for the cloud we are currently working on.)

When the folder is invoked, pytest will call the files that match ```test_*.py``` or ```*_test.py```. Here, I'm using ```test_*.py``` exclusively. The test files are grouped around cloud resources. For those functions that are not specific to a cloud (tools), I've lumped them into the ```test_<CloudCode>_tools.py``` file

## importing Cloud Module script
For the unit tests, the files need to Cloud Module (```az.py```). To do that the sys.path needs to be updated with the line:
```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
```
see: 
* https://docs.python.org/3/library/os.path.html#os.path.abspath
* https://docs.python.org/3/library/os.path.html#os.path.join
* https://docs.python.org/3/library/os.path.html#os.path.dirname
* https://docs.python.org/3/library/sys.html#sys.path
* https://docs.python.org/3/tutorial/datastructures.html (sys.path is a list which is where sys.path.indert comes from)
---

# How-To
## Add a function/class to Cloud Module (i.e. az.py)
0) Create a feature branch to work in
1) Write pytests script, or add to an existing script based on the cloud resoruces.
   ex: if you are writing additional fucntionality for an existing resoruce, modify the existing resource test file. If you are writting code for a new resource, create a new file.
2) Add new tests (Don't modify old tests)
3) Add the various functions to the Cloud Module (i.e. az.py)
4) TEST
   a. if the tests fail, iterate over the tests until you get full success
6) Write Infrastructure tests to prove the resources are being created/edited/deleted correctly
5) Implement those functions/classes in your script.
7) TEST
   a. if the tests fail, iterate over the tests until you get full success
6) Create pull request and review with the team.

## Create a new script
0) Create a feature branch to work in
1) If you need additional functionality in the Cloud Module, go to 'Add a function/class to Cloud Module'
2) Write Infrastructure tests to prove the resources are being created/edited/deleted correctly
3) Create a new script that does what you need.
5) TEST
   a. if the tests fail, iterate over the tests until you get full success
4) Create a new jenkins file, or add the new script to an existing Jenkins file
5) TEST
   a. if the tests fail, iterate over the tests until you get full success
6) Create pull request and review with the team.

## Add a new cloud service 
0) Create a feature branch to work in
1) Write a Unit test script for the first (and only the first) resoruce in the new (yet to be created) cloud module.
   a. For this new cloud module, we want to write everything as a "minimal viable product" (the less code, the better). The reason for this is we need to get all the way to the end with unit tests, deployment script, infrastructre tests, before we can add any functionality. Once we've reached minimum functionality, we can iterate over 'Add a function/class to Cloud Module' until we have everything we need.
   b. The script name should be ```test_<cloud code>_<resource name>.py```
   c. The script should be placed in the ````\tests\python_unit_tests```` directory.
2) Create a new Cloud Module file
   a. The module file name should be ```<cloud code>.py```
3) Write the code for the the first (and only the first) resoruce in the new cloud in the new Cloud Module.
4) TEST
   a. if the tests fail, iterate over the tests until you get full success
6) Create a new infrastructure test file for this could and this resource.
   a. The script name should be ```test_<cloud code>_<resource name>.py```
   b. The script should be placed in the ````\tests\infrastructure_tests```` directory.
5) Write infrastructer tests for the new resource in the new cloud
6) Write a deploy script for the new cloud that implements you new classes/functions in the new Cloud Module
7) TEST
   a. if the tests fail, iterate over the tests until you get full success
8) Create a new set of jenkins files (as appropriate). There should be at least the "OpsTesting" jenkins file to run tests through jenkins. There should be a maximum of 5 jenkins files one for each environment:
   a. Dev
   b. Test
   c. Stage
   d. Prod
9) Edit the jenkins file to do everything it needs to leveraging the new script (step 6 above) and run
10) TEST
   a. if the tests fail, iterate over the tests until you get full success
11) Iterate over 'Add a function/class to Cloud Module' to add new functionality.




# REFERENCES
## Python Tutorial
 - https://docs.python.org/3/tutorial/index.html
## Python Standard Library
 - https://docs.python.org/3/library/index.html#the-python-standard-library
### File and Directory Access :
 - https://docs.python.org/3/library/os.path.html#module-os.path
 - https://docs.python.org/3/library/sys.html#sys.path

## File and Folder Structure
 - https://docs.python-guide.org/writing/structure/

## Testing
### Test file structure
 - https://docs.python-guide.org/writing/structure/#test-suite

### PyTest
 - https://docs.pytest.org/

### PyLint
 - https://pylint.pycqa.org/

