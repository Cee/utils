#!/usr/bin/python
"""
Creates an html page from a template file.
"""

import sys
from pylib.create_page import create_page

if len(sys.argv) < 2:
    print("Must supply a page name.")
    exit(1)

page_nm = sys.argv[1]  # type: str
link = None
if len(sys.argv) > 2:
    link = sys.argv[2]
    sys.stderr.write("Link is " + link + "\n")

create_page(sys.stdin, sys.stdout, page_nm, link_insert=link)
