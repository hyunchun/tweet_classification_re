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
<<<<<<< 2ec6dd37461e852b06d33d75424a8a0fc8ea3f71
    label_dict = {}
=======
    category_list = {}
>>>>>>> tweet_100 folder added
    count = 0
    for line in inFile:
        count += 1
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)
<<<<<<< 2ec6dd37461e852b06d33d75424a8a0fc8ea3f71
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
=======

        category = tweet['category']
        if category not in category_list:
            category_list[category] = 1;
        else:
            category_list[category] += 1;

    for word in category_list:
        print("%s: %s" %(word, category_list[word]))
>>>>>>> tweet_100 folder added
    inFile.close()
    print("%s lines read" %(count))

 # ---------------------- #
if __name__ == "__main__":
    main()
