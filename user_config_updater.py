"""
A Module to update the user configuration file to set a custom path for any file-type
"""

from folder_cleaner import get_file_paths
import user_config_constants as ucc
import utils


def print_paths(available_paths, user_path):
    if user_path != ucc.NOT_AVAILABLE:
        is_usr_path = True
    else:
        is_usr_path = False

    print('*' * 20)
    print('Available Default Paths')
    for i, key in enumerate(available_paths.keys()):
        available_path = f"{key}) '{available_paths[key]}'"
        if not is_usr_path and i == 0:
            available_path += " - [CURRENT PATH]"
        print(f"{key}) {available_paths[key]}")

    if is_usr_path:
        print(
            f"n) Path you configured already - '{user_path}' - [CURRENT PATH]")
    print('*' * 20)


if __name__ == '__main__':
    ext = input('Enter the file type you want to configure: ').lower()

    user_config_fp = 'userFileTypesConfig.json'
    default_config_fp = 'fileTypesConfig.json'

    user_config = utils.load_json(user_config_fp)
    default_config = utils.load_json(default_config_fp)

    user_path = user_config.get(ext, ucc.NOT_AVAILABLE)

    default_paths = []
    get_file_paths(default_config, ext, default_paths)

    if len(default_paths) > 0:
        default_paths = utils.reverse_nested_list(default_paths)
        available_paths = {str(i): '\\'.join(default_path)
                           for i, default_path in enumerate(default_paths)}
        print_paths(available_paths, user_path)

    choice = input("Wanna Set a new Path [Y/N]?")
    if choice.lower() == 'y':
        choice = input(
            'Wanna set a path from a default paths/already set path [Y/N]?').lower()
        if choice == 'y':
            print_paths(available_paths, user_path)
            ip = input('Choose the path id [n to skip]: ').lower()
            if ip == 'n':
                print('SKIPPED')
            else:
                new_path = available_paths.get(ip)
                if not new_path is None:
                    user_config[ext] = new_path
                    utils.update_json(user_config_fp, user_config)
                    print(f"Path Updated for the type {ext}")
                    print(f"\tUpdated Path '{new_path}'")
        elif choice == 'n':
            new_path = input('Enter a Relative Path(s): ').strip()
            if new_path != '':
                user_config[ext] = new_path
                utils.update_json(user_config_fp, user_config)
                print(f"Path Updated for the type {ext}")
                print(f"\tUpdated Path '{new_path}'")
        else:
            print('Operation Failed! Rerun the Script again')
