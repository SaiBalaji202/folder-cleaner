"""
A Module which contains helper methods to clean a folder
"""

import os
import pathlib
import json

from os.path import exists
from pathlib import Path
from time import time
from multiprocessing import Process

import spinner


def get_files(directory, files_only=False):
    """
    Returns a list of files(absolute path) from a directory.

    Parameters:
    ---
    directory: dict
        Directory to scan for files
    files_only: bool
        Flag value to decide whether to get files alone or files & directories (default False)
    """
    data = [os.path.join(directory, name) for name in os.listdir(directory)]
    # Filter just a file type
    if files_only:
        data = [d for d in data if os.path.isfile(d)]
    return data


def get_file_name(full_path):
    """
    Returns File Name from a path

    Parameters:
    ---
    full_path: str 
        full path of a file
    """
    return os.path.basename(full_path)


def get_extension(file):
    """
    Returns a File Extension

    Parameters:
    ---
    file: str 
        full path of a file / just a file name

    Example:
    ---
    get_extension('sample.py') => '.py'
    """
    return pathlib.Path(file).suffix


def get_extensions(file):
    """
    Returns all the File Extensions

    Parameters:
    ---
    file: str 
        full path of a file / just a file name

    Example:
    ---
        get_extensions('sample.tar.gz') => 'tar.gz'
    """
    return ''.join(pathlib.Path(file).suffixes)


def merge_dictionaries(d1, d2):
    """
    Merge two dictionaries into a single dictionary

    Parameters:
    ---
    d1: dict
        Reference of Dictionary 1, 
    d2: dict
        Reference of Dictionary 2
    """
    return {**d1, **d2}


def load_json(json_path):
    """
     Load a JSON data from the json_path and converts it to Python Dictionary.

     Returns dictionary version of the Json Data present inside a json_path

     Parameters:
     ---
     json_path: str
        File Path of a JSON to load

    """
    with open(json_path) as json_file:
        return json.load(json_file)


def update_json(json_path, json_data: dict, indentation=4):
    """
    Update a JSON File with a new updated JSON Data

    Parameters:
    ---
    json_path: str
        File Path of a JSON to be updated, 
    json_data: dict
        Updated JSON Content in a Python Dictionary Format, 
    indentation: number
        Indentation for a JSON File (default 4)
    """
    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=indentation)


def create_file(file_path, data=''):
    """
    Creates a File (with some default data), if not exists
    """
    if not exists(file_path):
        file = open(file_path, "w")
        file.write(data)
        file.close()


def reverse_nested_list(ll):
    """
    Reverse all lists inside a list

    list: list
        list-of-list to reverse
    """
    return [l[::-1] for l in ll if isinstance(l, list)]


def start_spinner(flag: bool, delay=.5, msg='PROCESSING'):
    """
    Uses spinner package to display spinner parallely and Returns the instance of a running spinner.

    Spin only if flag is True, else return None

    Parameters:
    ---
    flag: bool
        Flag that conditionally displays spinner.  Spinner will get displayed only if it is set to True
    delay: number
        No of seconds the cursor should remain in one direction        
    msg: str
        Message that should get logged along with the spinner
    """
    if flag:
        spnr = spinner.start_spinner(msg=msg)
        return spnr


def stop_spinner(spnr: Process, msg="done"):
    """
    Terminates the spinner process

    Parameters:
    ---
    spnr: Process
        Instance of the running spinner process
    msg: str
        Stop Message
    """
    if isinstance(spnr, Process):
        spinner.stop_spinner(spnr, msg)


def performance(func):
    """
    Decorator Method to know the no of seconds your method took to execute    
    """
    def wrap_func(*args, **kwargs):
        t1 = time()
        res = func(*args, **kwargs)
        t2 = time()
        print('took {t2 - t1} sec')
        return res
    return wrap_func
