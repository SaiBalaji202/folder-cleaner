import json
import os


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


if __name__ == '__main__':
    with open('fileTypesConfig.json') as types_file:
        file_type_info = json.load(types_file)
        file_path = []
        ext = 'csv'
        if get_file_path(file_type_info, ext, file_path):
            # Reversing the list of path to get the correct path
            file_path = file_path[::-1]
            print(file_path)
