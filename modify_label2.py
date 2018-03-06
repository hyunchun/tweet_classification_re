from __future__ import print_function
from __future__ import division

try:
    import json
except ImportError:
    import simplejson as json

import string
import sys
import os

def main():
    filename = sys.argv[1]
    
    inFile = open("%s" %(filename))
    output = ""
    category_choice = raw_input("content or type: ")
    chosen_label = raw_input("label: ")

    for line in inFile:
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)
        try:
            type_label = tweet["type_label"]
            content_label = tweet["content_label"]
        except:
            output += json.dumps(tweet)
            output += "\n"
            continue 

        # modify
        if category_choice == "content":
            if chosen_label == content_label:
                print("screen name: ", tweet["screen_name"])
                print("text: ", tweet["text"].encode(encoding="utf-8"))
                print("type label: ", tweet["type_label"])

                new_content_label = raw_input("new content label: ")
                
                if (new_content_label == "next") or (new_content_label == "no"):
                    print("no change\n")
                else:
                    tweet["content_label"] = new_content_label
        elif category_choice == "type":
            if chosen_label == type_label:
                print("screen name: ", tweet["screen_name"])
                print("text: ", tweet["text"].encode(encoding="utf-8"))
                print("content label: ", tweet["content_label"])
        
                new_type_label = raw_input("new type label: ")
                
                if (new_type_label == "next") or (new_type_label == "no"):
                    print("no change\n")
                else:
                    tweet["type_label"] = new_type_label
        
        # save to output
        output += json.dumps(tweet)
        output += "\n"

    os.remove(filename)
    with open(filename, "w") as f:
        f.write(output)
    f.close()


 # ---------------------- #
if __name__ == "__main__":
    main()
