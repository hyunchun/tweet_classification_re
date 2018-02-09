from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

def main():
    train_filename = sys.argv[1]
    inFile = open("%s" %(train_filename), "r")
    category_list = {}
    count = 0
    for line in inFile:
        count += 1
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)

        category = tweet['category']
        if category not in category_list:
            category_list[category] = 1;
        else:
            category_list[category] += 1;

    for word in category_list:
        print("%s: %s" %(word, category_list[word]))
    inFile.close()
    print("%s lines read" %(count))

 # ---------------------- #
if __name__ == "__main__":
    main()
