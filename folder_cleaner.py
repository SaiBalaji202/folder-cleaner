"""
A Module which contains helper methods to clean a folder
"""

import json
import os
from os.path import isfile, join, exists, basename
from pathlib import Path
import shutil

import spinner
import folder_cleaner_constants as fcc
import user_config_constants as usc
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
    ext = Path(file_name).suffix
    if ext.strip() == '':
        base_name = basename(file_name)
        if base_name == '.gitignore':
            ext = '.gitignore'
    return ext


def get_full_extension(file_name):
    """
    Returns a list of all the Extensions of a file.

    Parameters:
    ---
    file_name: str
        Name of the File to which you want to get the extension

    Example:
    ---
    get_full_extension('filename.clipflair.zip') => ['.clipflair', '.zip']
    """
    return Path(file_name).suffixes


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

    # E.g. PNG -> png
    search_type = search_type.lower()

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

    # E.g. PNG -> png
    search_type = search_type.lower()

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


def move_files_user_config(user_config: dict, files):
    """
    Move files to the corresponding folder path in the user_config dictionary

    Parameters:
    ---
    user_config: dict
        Dictionary that contains the details of file type and it's complete path, 
    files: list
        List of files to Move
    """
    for file in files:
        ext = get_extension(file)[1:]
        file_name = basename(file)
        folder_to_clean = Path(file).parent

        # Get path from the user_config for a file type
        user_file_path = user_config.get(ext.lower())
        if user_file_path is not None:
            new_dir = folder_to_clean
            if not user_file_path == usc.PARENT:
                new_dir = join(folder_to_clean, user_file_path)
            new_file = join(new_dir, basename(file))
            create_directory(new_dir)
            move_file(file, new_file)


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
    spnr = utils.start_spinner(log, msg=fcc.MSG_SET_ENV)

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


def clean_folder(config_json_path, user_config_file, folder_to_clean, log=False):
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

    # Starting Directory Scanning Spinner
    spnr = utils.start_spinner(log, msg=fcc.MSG_DIR_SCAN)

    # Getting all files from the directory to be scanned
    files = scan_directory(folder_to_clean)

    # Stopping Directory Scanning Spinner
    utils.stop_spinner(spnr)

    # Loading the User Config FileTypes JSON Data
    if not exists(user_config_file):
        utils.create_file(user_config_file, '{}')
    user_config = utils.load_json(user_config_file)
    user_types = get_user_file_types(user_config_file)

    # Loading the APP Generated FileTypes JSON Data
    file_type_info = utils.load_json(config_json_path)

    # Starting Folder Cleaner Spinner
    spnr = utils.start_spinner(log, msg=fcc.MSG_FILE_MOVE)

    # Move Files using user config
    move_files_user_config(user_config, files)

    # Filtering files
    files = filter(lambda file: get_extension(file)[1:] not in user_types,
                   files
                   )

    exceptional_files = {}
    # Looping over the files
    for file in files:
        # Getting the File Extension and removing . (E.g. .mp4 => mp4)
        ext = get_extension(file)[1:].lower()
        file_path = []

        user_file_path = user_config.get(ext.lower())
        if user_file_path:
            new_dir = folder_to_clean
            if not user_file_path == usc.PARENT:
                new_dir = join(folder_to_clean, user_file_path)
                new_file = join(new_dir, basename(file))
                create_directory(new_dir)
                move_file(file, new_file)
        # Getting the Path of the file based on it's extension (ext)
        elif get_file_path(file_type_info, ext, file_path):
            # Reversing the list of path to get the correct path
            file_path = file_path[::-1]
            new_dir = join(folder_to_clean, '\\'.join(file_path))
            new_file = join(new_dir, basename(file))
            create_directory(new_dir)
            move_file(file, new_file)
        else:
            map_file_to_file_type(exceptional_files, ext, file)

    # Stopping Folder Cleaner Spinner
    utils.stop_spinner(spnr)

    exceptional_file_types = [ext for ext in exceptional_files.keys()]

    if len(exceptional_file_types) > 0:
        set_path_to_user_settings(
            exceptional_file_types,
            user_config_file
        )

        files = [file for ext in exceptional_files.keys()
                 for file in exceptional_files[ext]]

        spnr = utils.start_spinner(log, msg=fcc.MSG_FILE_MOVE)
        # Loading the Updated User Config
        user_config = utils.load_json(user_config_file)
        # Moving all the Exceptional Files
        move_files_user_config(user_config, files)
        utils.stop_spinner(spnr)


def get_user_file_types(file_path):
    """
    Returns a list of file types from the file_path json file

    Parameters:
    ---
    file_path: str
        file path of a user_config JSON File
    """
    user_types_info = utils.load_json(file_path)
    return [file_type.lower() for file_type in user_types_info.keys()]


def map_file_to_file_type(exceptional_files: dict, file_type, file_path):
    """
    Add a file path of an exceptional file to the exceptiona_files dictionary to its corresponding key (file_type).


    Parameters:
    ---
    exceptional_files: dict
        Dictionary to store Exceptional FileTypes
    file_type: str
        Exceptional File Type (It will become key for a exceptional_files dictionary)
    file_path: str
        File Path of a Exceptional File (Value of the corresponding key of exceptional_files dictionary)
    """
    file_type = file_type.lower()
    # Get a list of file paths that a file_type key has.  If the file_type is new, returns a new empty list to store file_path
    files = exceptional_files.get(file_type, [])
    # Append file_path to the extracted files list
    files.append(file_path)

    # If the file_type is new, then add the file_type along with the new list of file_type to the exceptional_files dictionary
    if len(files) == 1:
        exceptional_files[file_type] = files


def get_path_from_user_settings(user_config: dict, search_type):
    """
    Returns a Relative Path for storing particular type of File from the user_config dict

    Parameters:
    ---
    user_config: dict
        Dictionary that contains the details of User Configuration
    search_type: str
        file_type to search for
    """
    return user_config.get(search_type)


def set_path_to_user_settings(file_types, user_config_file_path):
    """
    Let's the end-user to set a file path for the file_types (new exceptional file_types).  
    Updates the user_config_file with the new file_type and the path the user sets.

    Parameters:
    ---
    file_types: list
        List of new exceptional file_types
    user_config_file_path: str
        Path of the user_config JSON file
    """
    path_info = {}
    print()
    print(
        f"OOPS! Unable to find path for few files types like ( {', '.join(file_types)} )"
    )
    print('Please Provide Your Input for those File Types')
    if input('Wanna Continue [Y/N]?').lower() == 'y':
        print('*' * 10)
        print('*' * 10)
        print('Press s to Skip your Input')
        print('Press p (or) ENTER for directly storing the file in its Parent Directory')
        print('*' * 10)
        print('*' * 10)
        total_extensions = len(file_types)
        for i, extension in enumerate(file_types):
            print(f"[{i + 1}/{total_extensions}] - {extension}")
            path = input('\tRelative Path: ')
            if path.lower() == 's':
                print('\t\tIGNORED')
                continue
            elif path == '' or path.lower() == 'p':
                path = usc.PARENT
            path_info[extension] = path
        print('*' * 10)
        existing_path_info = utils.load_json(user_config_file_path)
        # Merging the current configuration the user enters with the existing user configuration
        updated_path_info = utils.merge_dictionaries(
            existing_path_info, path_info)
        # Updating the user_config file with the updated configuration
        utils.update_json(user_config_file_path, updated_path_info)


if __name__ == '__main__':
    backup_directory = 'D:\\Folder to Clean - Copy'
    directory = 'D:\\Folder to Clean'

    set_up_test_folder(
        old_folder=backup_directory,
        new_folder=directory,
        log=True
    )

    clean_folder(
        'fileTypesConfig.json',
        'userFileTypesConfig.json',
        'D:\\Folder to Clean',
        log=True
    )
