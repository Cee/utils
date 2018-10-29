#!/usr/bin/python
import os
import argparse
ARG_ERROR = 1  # type: int

"""
Note: code will index any word containing keyword as substring.
eg: DRY

will index: DRYwasher, DRY?, DRY!!, DRY., DRY

for testing run:
(python3 gloss_links.py test_data/gloss_key.txt test_data --lf "test_data/gloss_links_inp1.txt" "test_data/gloss_links_inp2.txt")

Each file is opened only once now.
The data structure used in new version is a bit complicated:
-> keyword_context is a dictionary where key is key/glossary from gloss_list and value is another dictionary
-> in the nested dictionary key is name of files and value is list of context for that file. 
{keyword: {filenm:[context,...,contxt],..., filenm:[context,...,contxt]},.....,keyword: {filenm:[context,contxt],..., filenm:[context,context]}}

"""

def process_file(filenm, keyword_context, gloss_list):
    """
    Args: filenm and contexts_per_file
    returns: None
    """
    try:
        with open(filenm, 'r') as txt:
            for keyword in gloss_list:
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
                            
                            if keyword not in keyword_context:
                                keyword_context[keyword] = {}

                            file_per_keyword = keyword_context[keyword]
                            if filenm not in file_per_keyword:
                                keyword_context[keyword][filenm] = []
                            
                            keyword_context[keyword][filenm].append(context)
                txt.seek(0)
    
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


def output_context(outdir,keyword_context):
    """
        output context of a keyword
        Args: outdir, keyword, context
        Returns: None
    """
    for keyword in keyword_context:
        output_name = outdir + "/" + keyword + ".txt"
        with open(output_name,'w') as f:
            f.write(keyword + " occurs in: \n")
            temp = keyword_context[keyword]
            for filenm, context_list in temp.items():
                for context in context_list:
                    f.write("    " + filenm + ": " + context +"\n")
                f.write("\n")


if __name__ == '__main__':
    # get command line params:
    (keyword_file, outdir, file_list) = process_args()

    contexts_per_file = {}
    gloss_list = []
    keyword_context = {}
    # first get all the gloss keywords
    with open(keyword_file,'r') as gloss:
        for key in gloss:
            key = key.strip()
            gloss_list.append(key)

    for file in file_list: # look for keywords in all files
        process_file(file, keyword_context, gloss_list)
    
    output_context(outdir, keyword_context)

