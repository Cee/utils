"""
Script to check spellings of words in the web page. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser
import string
import re
import os.path
import argparse

try:
    from typing import List, Set
except ImportError:
    print(
        "WARNING: Typing module is not found! Kindly install the latest "
        "version of python!")

ARG_ERROR = 1  # type: int
SPELL_ERROR = 2  # type: int


def is_word(s, search=re.compile(r'[^a-zA-Z-\']').search):
    return not bool(search(s))


def check_file(*files):
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)


class OurHTMLParser(HTMLParser):
    def __init__(self):  # type: () -> None
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_data(self, data):  # type: (str) -> None
        web_page_words = data.split()  # type: List[str]

        for web_page_word in web_page_words:
            # strip other punctuations
            word = web_page_word.strip(string.punctuation).strip()  # type :str
            if not is_word(web_page_word):
                continue
            if len(web_page_word) == 1:
                continue
            if not strict_mode and word[0].isupper():
            	continue
            lower_word = word.lower()  # type: (str)
            if lower_word not in d:
                valid = False  # type: bool
                while not valid:
                    response = input("Do you want to add %s to dictionary?("
                                     "yes/no/skip)\n" % word)
                    # 'yes' to improve dictionary
                    if response.lower() == 'yes':
                        added_words.add(lower_word)
                        d.add(lower_word)
                        valid = True
                    # 'skip' unique strings (checksum/names) but not errors
                    elif response.lower() == 'skip':
                        valid = True
                    # 'no' if it is really a typo
                    elif response.lower() == 'no':
                        global saw_error  # type :bool
                        valid = True
                        saw_error = True
                        print("ERROR: " + word + line_msg())
                    else:
                        print("Invalid response, Please try again!")


exit_error = False
strict_mode = False
file_nm = None
main_dict = None
custom_dict = None

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_nm", help="html file to be parsed")
    arg_parser.add_argument("main_dict", help="main dictionary file")
    arg_parser.add_argument("custom_dict", help="custom dictionary file")
    arg_parser.add_argument("-e", help="enable exit error", action="store_true")
    arg_parser.add_argument("-s", help="strict mode checks capitalized words", action="store_true")
    args = arg_parser.parse_args()
    exit_error = args.e
    strict_mode = args.s
    file_nm = args.file_nm
    main_dict = args.main_dict
    custom_dict = args.custom_dict

# if len(sys.argv) != 4:
#    print("USAGE: html_spell.py fileToProcess mainDictionary customDictionary")
#    exit(ARG_ERROR)

check_file(file_nm, main_dict, custom_dict)
line_no = 0  # type :int
saw_error = False  # type: bool
d = set()  # type: Set[str]
added_words = set()  # type: Set[str]
code_tag_on = False  # type:bool
parser = OurHTMLParser()


def line_msg():  # type: () -> str
    return " at line number " + str(line_no)


# Loading words from main Dictionary into the python set data structure
with open(main_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())


# Loading words from custom Dictionary into the python set data structure
with open(custom_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())

with open(file_nm, "r", ) as f:
    for line in f:
        if "<code>" in line:
            code_tag_on = True

        if "</code>" in line:
            code_tag_on = False
            continue

        if not code_tag_on:
            parser.feed(line)
        line_no += 1

with open(custom_dict, 'a+') as f:
    f.writelines(i + '\n' for i in added_words)
    added_words.clear()

if saw_error and exit_error:
    exit(SPELL_ERROR)
else:
    exit(0)

