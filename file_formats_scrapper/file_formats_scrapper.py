from multiprocessing import Process
from pprint import pprint
import json

import requests
from bs4 import BeautifulSoup

from file_formats_scrapper.utils import Utils


class FileFormatsScrapper():
    """
        Class to scrap data from https://en.wikipedia.org/wiki/List_of_file_formats
    """

    __MSG_GEN_JSON = 'Generating Filetypes JSON'
    __MSG_JSON_SCRAPPED = '✓ JSON Generated Successfully :)'

    def __init__(self):
        self.__url = 'https://en.wikipedia.org/wiki/List_of_file_formats'
        self.__soup = self.__get_soup()
        self.__NOT_A_FILE_TYPES = ['see also', 'references', 'external links']
        self.__TOC_SELECTOR = '#toc > ul'
        self.__TOC_TEXT_SELECTOR = '.toctext'
        self.__file_type_info = {}

    def scrap(self, spin=False):
        """
            Scrap all the file formats from self.url and returns a result in the JSON format
            Returns the scrapped file_types JSON Object

            Parameters:
            ---
            spin: bool
                Flag that decides whether to display a spinner or not (default False)
        """

        # Start Spinning
        spnr = Utils.start_spinner(spin, 
                msg=FileFormatsScrapper.__MSG_GEN_JSON)

        # Get a soup to parse a HTML of the Site
        soup = self.__get_soup()

        # Selector to fetch the Table of Conetents page (to fetch type and sub-types)
        file_types = soup.select_one(self.__TOC_SELECTOR)
        self.__extract_data_from_a_tag(file_types)

        # Stop Spinning
        Utils.stop_spinner(spnr, msg=FileFormatsScrapper.__MSG_JSON_SCRAPPED)

        # Return the file_types JSON object
        return self.__file_type_info

    def __clean_type(self, type_name):
        """
        Returns a file_type by Removing the unnecessary leading and trailing spaces and lower the type

        Parameters:
        ---
            type_name: str
                file type to clean

        Example:
        ---
        self.__clean_type('<<space>>.doc<<space>>') => '.doc'
        """
        return type_name.strip().lower()

    def __clean_file_type(self, file_type):
        """        
        Returns a file_type by Removing . from the extension

        Parameters:
        ---
            file_type: str
                file type to clean

        Example:
        ---
        self.__clean_file_type('.docx') => 'docx'
        self.__clean_file_type('.PPTX') =>  'pptx'            
        """
        file_type = self.__clean_type(file_type)
        if not len(file_type.split(' ')) > 1:
            if file_type and file_type[0] == '.':
                file_type = file_type[1:]
            return file_type

    def __extract_data_from_a_tag(self, selector_tag, keys=None):
        """
            Extract all the type name (E.g. Program) and the sub-type name (E.g. Python) from the selector and update the self.file_type_info dictionary.
            If a root type name is Program, then it has lot of sub-types like C, C++, Java, Python, etc.
            Using this type and the sub-type name, we can create a folder to store the corresponding files in it.
            Used to group our File.

            Parameters:
            ---
            selector_tag: Tag 
                BeautifulSoup Tag of <ul/> tag
            keys: list
                List of keys, which represent a nested keys of a single item
                    keys = [Program, Python]
                    keys = [Program, C]       
        """
        keys = keys or []
        file_types = selector_tag.find_all('li', recursive=False)

        # Each type may have a sub-type too
        for file_type in file_types:
            type_name = file_type.select_one(
                self.__TOC_TEXT_SELECTOR).getText()
            # if the fetched data is a valid file type
            if self.__clean_type(type_name) not in self.__NOT_A_FILE_TYPES:
                # Add the type name to the self.file_type_info
                keys.append(type_name)
                # Setting Value for the parent property.  E.g. Program: {}
                Utils.set_dict(self.__file_type_info, keys, {})

                # Fetching all the sub-types of a current type
                # E.g. Program => Python
                sub_types = file_type.find_all('ul', recursive=False)
                if len(sub_types) > 0:
                    # Adding a sub_types key for a root file_type
                        # E.g. Program: {sub_types: {}}
                    keys.append('sub_types')
                    # Adding sub_types to self.file_type_info
                    Utils.set_dict(self.__file_type_info, keys, {})

                    # Iterating through all the sub_types
                    for sub_type in sub_types:
                        # Recursively call extract_data_from_a_tag() to extract all the sub_type info
                        self.__extract_data_from_a_tag(
                            selector_tag=sub_type, keys=keys)
                    # Removing the sub_types key
                    keys.pop()

                # Fetching all the direct types info
                # E.g. Python => [.py, .pyc]
                keys.append('types')

                # The Page stores all the types into the tag that has the file type name (seperated by _ instead of space) as its id
                # E.g. types of 'web page' will be stored inside the tag that has a id 'web_page'
                selector = f"[id='{Utils.replace_white_space(type_name)}']"

                Utils.set_dict(self.__file_type_info, keys,
                               self.__extract_types_from_a_selector(selector))
                # Popping the types key
                keys.pop()

                # Popping the type_name key
                keys.pop()

    def __extract_types_from_a_selector(self, css_selector):
        """
            Extract and returns all file types from the parent tag, that you specified by a css_selector
            Returns => file_types => List of file types

            Parameters:
            ---
            css_selector: str 
                CSS Selector for a parent tag that contains all the valid file types            
        """
        element = self.__soup.select_one(css_selector)
        # parent = element.parent

        file_types = []
        headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        element_to_process = element.parent
        # Process types from element_to_process until it doesn't become heading (which represents the next category or the next sub-category)
        while element_to_process.next_sibling is not None and element_to_process.next_sibling.name not in headings:
            # ul > li
            element_to_process = element_to_process.next_sibling
            if element_to_process.name == 'ul':
                # Fetch the direct li, without fetching the sub-category li
                lis = element_to_process.findChildren('li', recursive=False)
                for li in lis:
                    unexpected_child_types = li.findChildren(
                        'ul',
                        recursive=False)
                    # If there is no unexpected child sub-category
                    if not len(unexpected_child_types) > 0:
                        # Here the file_types are normal strings
                        for file_type in self.__get_types_from_li(li.getText()):
                            # Cleaning file types
                            # E.g. '  .doc ' => 'doc'
                            file_type = self.__clean_file_type(file_type)
                            if file_type:
                                file_types.append(file_type)
                    else:
                        # Here the file_types are dictionary

                        # Getting the sub-type name alone, without description
                        sub_type_name = self.__get_subtype_name_without_desc(
                            li.getText())
                        # Get all the unexpected nested types
                        unexpeced_nested_types = self.__get_unexpected_nested_ul_types(
                            parent_tag=li,
                            parent_name=sub_type_name)
                        if unexpeced_nested_types:
                            file_types.append(unexpeced_nested_types)

            # div > table >li
            elif element_to_process.name == 'div':
                table = element_to_process.findChildren('table')
                if table:
                    # Getting all li inside table
                    lis = element_to_process.findChildren('li')
                    for li in lis:
                        # Getting all types from a row / li
                        for file_type in self.__get_types_from_li(li.getText()):
                            # Clean and store file_type
                            file_type = self.__clean_file_type(file_type)
                            if file_type:
                                file_types.append(file_type)

        return file_types

    def __get_subtype_name_without_desc(self, sub_type):
        """
            Returns a type name without it's description and it's subtypes

            Parameters:
            ---
            sub_type: str
                Sub Type with its description
            Example:
            ---
            E.g. self.__get_subtype_name_without_desc('Document - Document Files
                                                .doc - document
                                                .docx - document') => 'Document'
        """
        sub_type = Utils.fetch_substring(sub_type, '\n')
        # Remove unicode hyphen
        sub_type = Utils.fetch_substring(sub_type, '\u2013')
        sub_type = Utils.fetch_substring(sub_type, '\u2212')

        # Remove unicode double hyphen
        sub_type = Utils.fetch_substring(sub_type, '\u2014')
        # Remove ascii hyphen
        sub_type = Utils.fetch_substring(sub_type, '-')
        return sub_type.strip()

    def __get_types_from_li(self, li):
        """
        Returns all file types seperated by comma from a single <li /> / single row

        Parameters:
        ---
            li: str
                <li /> string
        """
        # Handling Types
        types_word = li

        # Remove unicode hyphen
        types_word = Utils.fetch_substring(types_word, '\u2013')
        types_word = Utils.fetch_substring(types_word, '\u2212')

        # Remove unicode double hyphen
        types_word = Utils.fetch_substring(types_word, '\u2014')
        # Remove ascii hyphen
        types_word = Utils.fetch_substring(types_word, '-')

        # Fetch types between paranthesis.
        # E.g. "Document (.doc, .docx)" => ".doc, .docx"
        open_paranthesis = types_word.find('(')
        close_paranthesis = types_word.find(')')
        if open_paranthesis != -1 and close_paranthesis != -1:
            if len(types_word[open_paranthesis + 1: close_paranthesis].split(',')) > 1:
                # E.g. "CLIPFLAIR (.clipflair, .clipflair.zip)" => ".clipflair, .clipflair.zip"
                types_word = types_word[open_paranthesis +
                                        1: close_paranthesis]
            else:
                # E.g. "ASS (also SAS)" => "ASS"
                types_word = types_word[:open_paranthesis]
                # E.g. "MPQ Archives (.mpq)" => "MPQ" (and not "MPQ Archives")
                types_word = types_word.split(' ')[0]

        # rename or to , => E.g. ".asc or .txt" => ".asc, .txt"
        types_word = types_word.replace(' or ', ', ')

        # rename / to , => E.g. "chp / pub / sty" => "chp , pub , sty"
        types_word = types_word.replace('/', ', ')

        # Rename all , + space to ,
        types_word = types_word.replace(', ', ',')

        # split based on , and
        types = [type_word.strip() for type_word in types_word.split(',')]
        if types[-1].find('and ') == 0:
            types[-1] = types[-1][len('and '):]

        return types

    def __get_unexpected_nested_ul_types(self, parent_tag, parent_name):
        """
            Returns a nested ul that may come unexpectedly inside a types array
            Returns => a dictionary that contains the nested type info & its corresponding sub-typ info

            Parameters:
            ---
                parent_tag: Tag 
                    BeautifulSoup Tag of a li which contains that unexpected nested types
                parent_nmae: str
                    Name of the parent_tag
        """
        # Getting a nested ul
        ul = parent_tag.select_one('ul')
        lis = ul.findChildren('li', recursive=False)

        file_types = []
        nested_types = []

        # Iterating over all the individual types
        for li in lis:
            # Get all types from a single row / single li
            # E.g. Python (.py, .pyc) => [.py, .pyc]
            for file_type in self.__get_types_from_li(li.getText()):
                # If there is no sub-type
                if not len(li.findChildren('ul')) > 0:
                    # Clean the File Type.  E.g. '.doc' => 'doc'
                    file_type = self.__clean_file_type(file_type)
                else:
                    # Getting the name of sub-type by removing the description
                    sub_type_name = self.__get_subtype_name_without_desc(
                        li.getText())
                    # Call this method recursively to get all the nested sub-types
                    nested_types = self.__get_unexpected_nested_ul_types(
                        li, sub_type_name)

                # Storing a file_type, if available
                if file_type:
                    file_types.append(file_type)
                    file_type = None
                # Storing nested_types, if available
                if nested_types:
                    file_types.append(nested_types)
                    # Clearing the nested_types, so that it won't be available for the next iteration.
                    # If we haven't clear it, nested_types will carry it's value for the next iteration too.
                    nested_types = []

        return {
            parent_name: {
                'types': file_types
            }
        }

    def __get_soup(self):
        """
            Send request to the URL and get a soup object that represents the structure of the URL
        """
        response = requests.get(
            'https://en.wikipedia.org/wiki/List_of_file_formats')
        return BeautifulSoup(response.text, 'html.parser')
