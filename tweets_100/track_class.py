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
            type_label = tweet['type_label']
            content_label = tweet['content_label']
            label_tuple = (type_label, content_label)
            if label_tuple not in label_dict:
                label_dict[label_tuple] = 1
            else:
                label_dict[label_tuple] += 1
        except:
            break
    for label_tuple in label_dict:
        print("%s, %s: %s" %(label_tuple[0], label_tuple[1], label_dict[label_tuple]))
    inFile.close()
    print("%s lines read" %(count))

 # ---------------------- #
if __name__ == "__main__":
    main()
