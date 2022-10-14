# PYTHON_EXAMPLE
Testing a Jenkins env. with Python script to Azure using pylint and pytest

# FILES AND FOLDERS
* ./requirements.txt - List of modules required by this project to be called by pip for installation
* ./azure.py - Module of Azure classes and methods used for this project  
* ./tests - Folder for all files related to testing
* ./tests/python_unit_tests/__init__.py - for some reason, this file is needed. pytests won't work without it. it is empty.
* ./tests/python_unit_tests/context.py - Used for importing root folder modules (./azure.py in this example)
* ./tests/python_unit_tests/test_azure_storage_account.py - Test script for Storage Account code within the azure module.

# SETUP
## pylint
configuration file created from this call:
```cmd
pylint --disable=no-else-return,trailing-whitespace --generate-rcfile --max-line-length 140 > pylint.config2
```
Then the file was paired down to just the parts that were configured, leaving the rest of it configured to use
the defaults.


# PROCESS
1. pylint
   1. pylint --rcfile .\pylint_config azure
   2. pylint --rcfile .\pylint_config tests\test_azure_tools.py
2. tests
   1. py -m pytest .\tests\test_azure_tools.py -or- py -m pytest -v

---


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

---
---

# Notes
* https://docs.python-guide.org/writing/structure/#test-suite using a context.py file for test scripts.
* https://docs.python-guide.org/writing/structure/#makefile - using make to build/test the environment.