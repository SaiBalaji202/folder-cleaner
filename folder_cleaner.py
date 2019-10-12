import json
import os


class FolderCleaner(object):
    """
    Class that does all the folder cleaning tasks like
        finding folder path for a file extension,
        moving files to the corresponding folder, etc.
    """

    def __init__(self, file_type_info):
        self.file_type_info = file_type_info

    def get_path(self, file_path_info, folders):
        pass

    def get_full_path(self, file_path):
        pass

    def find_item_in_dict(self, file_type_info, result, search_key):
        # Boolean Value to check wheter a file_type is found/not
        found = False

        # Iterating over the file_type_info dictionary to get the file_type path
        for key, value in file_type_info.items():

            # Checking in direct types
            if 'types' in file_type_info[key]:
                # Updating path in result list, if file_type is found
                if search_key in file_type_info[key]['types']:
                    result.append(key)
                    found = True
                else:
                    # If direct types contains unexpected nested types, then recursively call the same method to check for the type inside that unexted nested types
                    for file_type in file_type_info[key]['types']:
                        if type(file_type) == type({}):
                            # Updating path in result list, if file_type is found
                            if(self.find_item_in_dict(
                                    file_type, result, search_key)):
                                result.append(key)
                                found = True
                                break

            # Recursively call the same method to check for the type inside a sub-type dictionary
            if 'sub_types' in file_type_info[key]:
                # Updating path in result list, if file_type is found
                if self.find_item_in_dict(file_type_info[key]['sub_types'], result, search_key):
                    result.append(key)
                    found = True
                    break
        return found


if __name__ == '__main__':
    with open('fileTypesConfig.json') as types_file:
        file_type_info = json.load(types_file)
        folder_cleaner = FolderCleaner(file_type_info)
        path = []
        print(folder_cleaner.find_item_in_dict(
            file_type_info, path, 'aspx'))
        print(path[::-1])
