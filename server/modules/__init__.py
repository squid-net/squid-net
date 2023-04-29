import os
import importlib

# Get all files.
views = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.endswith(".py") and f != "__init__.py"]

# Import all files from modules folder.
for view in views:
    # Get the directory path and replace backslashes with forward slashes
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

    # Split the path and construct the module name
    module_name = dir_path.split('/')[-1] + "." + view[:-3]

    # Import the module
    importlib.import_module(module_name)
    print('App imported ' + view + ' successfully.')