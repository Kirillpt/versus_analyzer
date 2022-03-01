#!/usr/bin/env python
import argparse
import glob
from versus_analyzer import *

versus_storage = VersusStorage()

def init_versus_analyzer():
    # loads files to versus_analyzer
    files_in_dir = glob.glob("battles/*")
    for cfile in files_in_dir:
        versus_text = open(cfile).read()
        file_name = cfile.split("/")[1]
        versus_storage.add_versus(file_name, versus_text)

def run_search(target_word):
    artists = versus_storage.get_artists_used_word(target_word)
    if len(artists) == 0:
        print("Artists not found")
    else:
        print("Found {} artists".format(len(artists)))
        print("-"*15)
    for artist in artists:
        print(artist)

def run_plagiat_test():
    plagiat_result = versus_storage.find_all_plagiat()
    for (first_word, second_word), names in plagiat_result.items():
        if len(names) == 1:
            continue
        print("Rhyme \"{}  <->  {}\" was used {} times, by this guys:".format(
            first_word,second_word, len(names)
        ))
        for mc in names:
            print(" "*4 + mc)
        print()

    pass


arg_parser = argparse.ArgumentParser(
    description='Analyze versus battles for plagiat and search what artists used that specific word')

arg_parser.add_argument("--plagiat", action='store_true',
   help="Use this flag to find some plagiat")

arg_parser.add_argument("--search", "--search",
   help="Enter word, to find what artists used it in versus")

params = vars(arg_parser.parse_args())

init_versus_analyzer()

if params["plagiat"] == True:
    print("RUN PLAGIAT TEST")
    run_plagiat_test()

if params["search"] != None:
    print("#"*80)
    print("Search For \"{}\" Word".format(params["search"]))
    print("#"*80)
    run_search(params["search"])
    print("#"*80)

