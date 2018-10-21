#!/usr/bin/python
import os
import argparse
ARG_ERROR = 1  # type: int

"""
Note: code will index any word containing keyword as substring.
eg: DRY

will index: DRYwasher, DRY?, DRY!!, DRY., DRY

for testing run:
(python3 gloss_links.py test_data/gloss_key.txt test_data/test_data --lf  
test_data/gloss_links_test1.txt  test_data/gloss_links_test2.txt)

output: 

test_data/<output directory>.<keyword>.txt
test_data/<output directory>.<keyword>.txt

--to dicuss:
* where should output file be?
* where to include context in file links. 

"""

def process_file(filenm, contexts_per_file):
    """
    Args: filenm and contexts_per_file
    returns: None
    """
    try:
        with open(filenm, 'r') as txt:
            for line in txt:
    
                # splits into a list
                if keyword in line:
                    line = line.strip().split(" ")
                    context = None
                    index_list = []
    
                    # iterate over list to handle edge case when 
                    # keyword ends with punctuation
                    for index, word in enumerate(line):
                        if keyword in word:
                            index_list.append(index)
    
                    for index in index_list:
                        # if keyword appears more than once in a line
                        key_index = index
    
                        if 0 < key_index < len(line) - 1:
                            context = (line[key_index-1] + " " +
                                    line[key_index] + " " +
                                    line[key_index+1])
    
                        elif key_index == 0:
                            if len(line) > 1:
                                context = (line[key_index] + " " + 
                                        line[key_index+1])
                            else:
                                context = line[key_index]
    
                        elif key_index == len(line) - 1:
                            context = (line[key_index - 1] + " " + 
                                    line[key_index])
                        contexts_per_file[file].append(context)
    except IOError as ioe:
        print("Error opening file: %s; exception: %s", (filenm, str(ioe)))
        return None

def process_args():
    """
    Parses command line args and returns:
        keyword_file, file_list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("gloss_key")
    arg_parser.add_argument("outdir")
    arg_parser.add_argument(
        "--lf", # you need to add "--lf" flag in command line
        nargs="*",
        type=str,
        default=[],
    )
    args = arg_parser.parse_args()
    keyword_file = args.gloss_key
    outdir = args.outdir
    file_list = args.lf
    return (keyword_file, outdir, file_list)


def output_context(outdir, keyword, contexts_per_file):
    """
        output context of a keyword
        Args: outdir, keyword, context
        Returns: None
    """
    output_name = outdir + "/" + keyword + ".txt"
    with open(output_name,'w') as f:
        for key, value in contexts_per_file.items():
            f.write(keyword + " occurs in: \n")
            for each_context in value:
                f.write("    " + key + ": " + each_context +"\n")
        f.write("  ")


if __name__ == '__main__':
    # get command line params:
    (keyword_file, outdir, file_list) = process_args()

# for debugging:
# print(list_files)
# list_files = list_files.strip('[]').split(',')

    contexts_per_file = {}
    gloss_list = []
    # first get all the gloss keywords
    with open(keyword_file,'r') as gloss:
        for key in gloss:
            key = key.strip()
            gloss_list.append(key)

    for keyword in gloss_list:
        for file in file_list: # look for keywords in all files
            contexts_per_file[file] = []
            process_file(file, contexts_per_file)

        output_context(outdir, keyword, contexts_per_file)
        contexts_per_file = {}  # blank to get ready for next keyword

"""
<-----Testing Optimization----->
for lineno, line in enumerate(lines, 1): # start counting at 0
    fields = line.split()
    try:
        count = int(fields[1])
        ...
    except ValueError as e:
        print('Line {}: Parse error: {}'.format(lineno, e))

from collections import defaultdict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)",

# remove punctuation from the string
no_punct = ""
for char in my_str:
   if char not in punctuations:
       no_punct = no_punct + char

# display the unpunctuated string
print(no_punct)

"""