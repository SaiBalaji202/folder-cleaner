import json
from file_formats_scrapper import FileFormatsScrapper

with open('fileTypesConfig.json', 'w') as fp:
    json.dump(FileFormatsScrapper().scrap_file_formats(), fp, indent=4)
