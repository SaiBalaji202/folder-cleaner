import os
import pathlib
import json
from multiprocessing import Process
import spinner


def get_files(directory, files_only=False):
    """
        Get absolute path of files from a directory.
        Returns => List of files

        directory => Directory to scan for files
        files_only => Default False - Get both the files and the directories
    """
    data = [os.path.join(directory, name) for name in os.listdir(directory)]
    # Filter just a file type
    if files_only:
        data = [d for d in data if os.path.isfile(d)]
    return data


def get_file_name(full_path):
    """
        Get File Name from a path

        full_path => full path of a file
    """
    return os.path.basename(full_path)


def get_extension(file):
    """
        Get a File Extension
        E.g. sample.py => .py

        file => full path of a file / just a file name
    """
    return pathlib.Path(file).suffix


def get_extensions(file):
    """
        Get all the File Extensions
        E.g. sample.tar.gz =>tar.gz

        file => full path of a file / just a file name
    """
    return ''.join(pathlib.Path(file).suffixes)

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
    """
    if isinstance(spnr, Process):
        spinner.stop_spinner(spnr, msg)

