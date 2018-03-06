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
    label_dict = {}
    count = 0
    for line in inFile:
        count += 1
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)
        try:
            print("text: ", tweet['text'])
            print("type_label: ", tweet['type_label'])
            print("content_label: ", tweet['content_label'])
            
        except:
            return
    inFile.close()

 # ---------------------- #
if __name__ == "__main__":
    main()
