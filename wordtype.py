#!/usr/bin/env python3

from PyDictionary import PyDictionary

import os, socket, time, nltk

nltk.download('averaged_perceptron_tagger')
dictionary = PyDictionary()
print("Init finished")

host = "127.0.0.1"
port = 1236

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        while(True):
            # lookup suggestions for single-word input strings
            try:
                input_term, source = s.recvfrom(1024)  # Network input
                input_term = input_term.decode()

                print(nltk.pos_tag(input_term))

                meaning = dictionary.meaning(input_term)
                if meaning == None:
                    s.sendto("0".encode(), source)
                else:
                    print("Meaning: {}".format(meaning))
                    wordtypes = meaning.keys()
                    print("Types: {}".format(wordtypes))

                    s.sendto(str(len(wordtypes)).encode(), source)
                    for wordtype in wordtypes:
                        print("wordtype: {}".format(wordtype))
                        s.sendto(wordtype.encode(), source)
            except Exception as e:
                print(e)
                time.sleep(1)
    
if __name__ == "__main__":
    main()
