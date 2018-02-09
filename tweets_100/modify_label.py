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
    selected = sys.argv[2]
    inFile = open("%s" %(filename))
    output = ""
    for line in inFile:
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)
        category = tweet['category']
        if category == selected:
            print("screen name: ", tweet['screen_name'])
            print("text: ", tweet['text'].encode(encoding="utf-8"))
            input_category = raw_input("Label: ")
            if (input_category == "next") or (input_category == "no"):
                print("no change\n")
            else:
                tweet['category'] = input_category
        output += json.dumps(tweet)
        output += "\n"

    os.remove(filename)
    with open(filename, 'w') as f:
        f.write(output)
    f.close()


 # ---------------------- #
if __name__ == "__main__":
    main()
