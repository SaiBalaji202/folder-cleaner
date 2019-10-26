"""
A Module to generate/update the fileTypesConfig.json.

It uses file_formats_scrapper package to generate/update the fileTypesConfig.json.
"""

import json
from file_formats_scrapper import FileFormatsScrapper

if __name__ == '__main__':
    with open('fileTypesConfig.json', 'w') as fp:
        # json.dump(FileFormatsScrapper().scrap_file_formats(), fp, indent=4)
        json.dump(FileFormatsScrapper().scrap(True), fp, indent=4)
