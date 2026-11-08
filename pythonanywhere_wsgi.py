"""Copy this file into the WSGI editor for the eyadelsafty account."""
import os
import sys

project_path = '/home/eyadelsafty/nyc_team5'
if project_path not in sys.path:
    sys.path.insert(0, project_path)
os.chdir(project_path)
from app import server as application
