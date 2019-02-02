#!/usr/bin/env python3

import os, socket, time

host = "127.0.0.1"
port = 1234

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

def main():
    # create object
    initial_capacity = 83000
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        while(True):
            # lookup suggestions for single-word input strings
            try:
                input_term, source = s.recvfrom(1024)  # Network input
                input_term = input_term.decode()
                print("Test2 Input: {}".format(input_term))
                # max edit distance per lookup
                # (max_edit_distance_lookup <= max_edit_distance_dictionary)
                max_edit_distance_lookup = 2
                suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
                suggestions = sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
                # display suggestion term, term frequency, and edit distance
                for suggestion in suggestions:
                    print("Test2 Output: {}, {}, {}".format(suggestion.term, suggestion.count, suggestion.distance))
                s.sendto(suggestions[0].term.encode(), source)

            except Exception as e:
                print(e)
                time.sleep(1)
    
if __name__ == "__main__":
    main()
