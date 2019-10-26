
from folder_cleaner import clean_folder
import sys

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) <= 1 or sys.argv[1].strip() == '':
        directory = input('Enter the Directory Path to clean: ').strip()
    else:
        directory = sys.argv[1].strip()

    if directory:
        clean_folder(
            'fileTypesConfig.json',
            'userFileTypesConfig.json',
            directory,
            log=True
        )
    else:
        print('Enter a Valid Directory Name!')
