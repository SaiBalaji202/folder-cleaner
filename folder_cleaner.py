"""
A Module which contains helper methods to clean a folder
"""

import json
import os
from os.path import isfile, join, exists, basename
from pathlib import Path
import shutil

import folder_cleaner_constants as fcc
import utils


def scan_directory(directory):
    """
    Returns all the files (only files) of a directory

    Parameters:
    ---
    directory: str
        complete path of a directory to be scanned
    """
    files = [join(directory, content) for content in os.listdir(
        directory) if isfile(join(directory, content))]
    return files


def create_directory(dir_full_name):
    """
    Creates a Hierarchy of Nested Directories if not exist

    Parameters:
    ---
    dir_full_name: str
        Complete path of a nested directories to be created
    """
    if not exists(dir_full_name):
        os.makedirs(dir_full_name)


def move_file(old_path, new_path):
    """
    Moves file from one path to another path

    Parameters:
    ---
    old_path: str
        Existing File Path (along with the file name)
    new_path: str
        New Path where the file is to be moved (along with the file name)    
    """
    os.rename(old_path, new_path)


def delete_directory(directory):
    """    
    Deletes a Directory along with its content

    Parameters:
    ---
    directory: str
        Full Path of the directory to be deleted
    """
    if exists(directory):
        shutil.rmtree(directory)


def get_extension(file_name):
    """
    Returns a Extension of a file

    Parameters:
    ---
    file_name: str
        Name of the File to which you want to get the extension.     

    Example:
    ---
    get_extension('filename.mp4') => '.mp4'
    """
    return Path(file_name).suffix


def get_file_path(file_type_info: dict, search_type, file_path):
    """
    A Method to get a complete hyerarchical path for a file based on it's type

    Parameters:
    --
    file_type_info: dict
        Parsed JSON Object that contains the details of all the possible file types
    search_type: str
        Type of the file you want to get a hyerarchical path
    file_path: list
        A list to store the result of this method call
    """
    # Boolean Value to check wheter a file_type is found/not
    found = False

    # Iterating over the file_type_info dictionary to get the file_type path
    for key, value in file_type_info.items():
        # Checking in direct types
        if 'types' in file_type_info[key]:
            # Updating path in result list, if file_type is found
            if search_type in file_type_info[key]['types']:
                file_path.append(key)
                found = True
                # Stop checking for another possible path by breaking from the loop
                break
            else:
                # If direct types contains unexpected nested types, then recursively call the same method to check for the type inside that unexted nested types
                for file_type in file_type_info[key]['types']:
                    if type(file_type) == type({}):
                        # Updating path in result list, if file_type is found
                        if(get_file_path(file_type, search_type, file_path)):
                            file_path.append(key)
                            found = True
                            break

        # Recursively call the same method to check for the type inside a sub-type dictionary
        if 'sub_types' in file_type_info[key]:
            # Updating path in result list, if file_type is found
            if get_file_path(file_type_info[key]['sub_types'], search_type, file_path):
                file_path.append(key)
                found = True
                break
    return found


def get_file_paths(file_type_info, search_type, file_paths):
    """
    A Method to get all the possible paths for a file based on it's type

    Parameters:
    --
    file_type_info: dict
        Parsed JSON Object that contains the details of all the possible file types
    search_type: str
        Type of the file you want to get a hyerarchical path
    file_paths: list 
        A list-of-list to store the result of this method call
    """
    # Boolean Value to check wheter a file_type is found/not
    found = False

    # Iterating over the file_type_info dictionary to get the file_type path
    for key, value in file_type_info.items():

        # Checking in direct types
        if 'types' in file_type_info[key]:
            # Updating path in result list, if file_type is found
            if search_type in file_type_info[key]['types']:
                # Adding New Path as a List
                file_paths.append([key])
                found = True
            else:
                # If direct types contains unexpected nested types, then recursively call the same method to check for the type inside that unexted nested types
                for file_type in file_type_info[key]['types']:
                    if type(file_type) == type({}):
                        # Updating path in result list, if file_type is found
                        if(get_file_paths(file_type, search_type, file_paths)):
                            # Updating the corresponding path (last path) in the list
                            file_paths[len(file_paths) - 1].append(key)
                            found = True
                            break

        # Recursively call the same method to check for the type inside a sub-type dictionary
        if 'sub_types' in file_type_info[key]:
            # Updating path in result list, if file_type is found
            if get_file_paths(file_type_info[key]['sub_types'], search_type, file_paths):
                # Updating the corresponding path (last path) in the list
                file_paths[len(file_paths) - 1].append(key)
                found = True
    return found


def set_up_test_folder(old_folder, new_folder, log=False):
    """
    Set up the testing environment to test the folder-cleaning feature

    Setup's a new_folder with mixed types of files that are copied from some folder (old_folder)

    Parameters:
    ---
    old_folder: str
        Source Folder Path from where the files should be copied
    new_folder: str
        Destination Folder Path to where the files should be pasted
    log: bool
        Diplay Spinner with the corresponding log message when doing the corresponding operation (default False)
    """
    # Starting Spinner
    spnr = utils.start_spinner(msg=fcc.MSG_SET_ENV)

    # Recreating a directory to clean by deleting it and creating it again
    delete_directory(new_folder)
    create_directory(new_folder)

    # Scanning all the files from the Source Directory
    files = scan_directory(old_folder)

    # Copying all the files from the Source Directory to the Directory to be cleaned
    for file in files:
        file_name = basename(file)
        new_file = join(new_folder, file_name)
        shutil.copyfile(file, new_file)

    # Stopping Spinner
    utils.stop_spinner(spnr)


def clean_folder(config_json_path, folder_to_clean, log=False):
    """
    Performs Folder Cleaning Operation

    Parameters:
    ---
    config_json_path: str
        Path of the JSON File that contains the details of all the possible file types.
        Use file_formats_scrapper package to generate this JSON file.
    folder_to_clean: str
        Path of folder to be cleaned
    log: bool
        Diplay Spinner with the corresponding log message when doing the corresponding operation (default False)
    """
    # Open the JSON File
    with open(config_json_path) as config_file:
        # Parsing the JSON File to a Python Type
        file_type_info = json.load(config_file)

        # Starting Spinner
        spnr = utils.start_spinner(msg=fcc.MSG_DIR_SCAN)

        # Getting all files from the directory to be scanned
        files = scan_directory(directory)

        # Stopping Spinner
        utils.stop_spinner(spnr)

        # Starting Spinner
        utils.start_spinner(msg=fcc.MSG_FILE_MOVE)

        # Looping over the files
        for file in files:
            # Getting the File Extension and removing . (E.g. .mp4 => mp4)
            ext = get_extension(file)[1:]
            file_path = []
            # Getting the Path of the file based on it's extension (ext)
            if get_file_path(file_type_info, ext, file_path):
                # Reversing the list of path to get the correct path
                file_path = file_path[::-1]
                # Generating the final directory path from the base directory + the generated file path
                new_dir = join(directory, '\\'.join(file_path))
                # Generating the final file path by new_dir + file_name
                new_file = join(new_dir, os.path.basename(file))
                # Creating a new_dir to move the file
                create_directory(new_dir)
                # Moving the file to it's corresponding directory
                move_file(file, new_file)

        # Stopping Spinner
        utils.stop_spinner(spnr)


if __name__ == '__main__':
    backup_directory = 'D:\\Folder to Clean - Source'
    directory = 'D:\\Folder to Clean'

    set_up_test_folder(
        old_folder=backup_directory, new_folder=directory, log=True)

    clean_folder('fileTypesConfig.json', "D:\\Folder to Clean",
                 log=True)
