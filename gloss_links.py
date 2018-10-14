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

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("gloss_key")
    arg_parser.add_argument("output")
    #arg_parser.add_argument("list_files")
    arg_parser.add_argument(
        "--lf", #you need to add "--lf" flag in command line
        nargs="*",
        type=str,
        default=[],
    )
    args = arg_parser.parse_args()
    keyword = args.gloss_key
    list_files = args.lf
    output_file = args.output

# print(list_files)
# list_files = list_files.strip('[]').split(',')

index_dict = {}
gloss_list = []
#first get all the gloss keywords
with open(keyword,'r') as gloss:
    for key in gloss:
        key = key.strip()
        gloss_list.append(key)

#this code is not so efficent now, CAN BE IMPROVED.
#because Professor changed requirements lately. 

for keyword in gloss_list:
    for file in list_files:
        try:
            with open(file, 'r') as txt:
                for line in txt:

                    # splits into a list
                    if keyword in line:
                        line = line.strip().split(" ")
                        context = None
                        index_list = []

                        #iterate over list to handle edge case when 
                        #keyword ends with punctuation
                        for index, word in enumerate(line):
                            if keyword in word:
                                index_list.append(index)
        
                        for index in index_list:
                            #if keyword appears more than once in a line
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
        
                            if file not in index_dict:
                                index_dict[file] = []

                            index_dict[file].append(context)

        except IOError as ioe:
            print("Error opening the file:", ioe)
            exit(1)
    
    output_name = output_file+"." + keyword + ".txt"
    with open(output_name,'w') as f:
        for key, value in index_dict.items():
            f.write(keyword + " occurs in: \n")
            for each_context in value:
                f.write("    " + key + ": " + each_context +"\n")
        f.write("  ")
        index_dict = {}
