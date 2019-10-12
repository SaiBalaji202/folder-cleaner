import json
from file_formats_scrapper import FileFormatsScrapper

if __name__ == '__main__':
    with open('fileTypesConfig.json', 'w') as fp:
        # json.dump(FileFormatsScrapper().scrap_file_formats(), fp, indent=4)
        json.dump(FileFormatsScrapper().scrap(), fp, indent=4)