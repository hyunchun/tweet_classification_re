from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

def main():
    train_filename1 = sys.argv[1]
    train_filename2 = sys.argv[2]
    inFIle1 = {}
    inFile1 = open("%s" %(train_filename1), "r")
    inFile2 = {}
    inFile2 = open("%s" %(train_filename2), "r").readlines()
    
    category_list1 = {}
    category_list2 = {}
    match_class = {}
    count = 0
    mismatch = 0

    for index, line in enumerate(inFile1):
        count += 1
        tweet1 = json.dumps(line)
        tweet1 = json.loads(tweet1)
        tweet1 = json.loads(tweet1)

        tweet2 = json.dumps(inFile2[index])
        tweet2 = json.loads(tweet2)
        tweet2 = json.loads(tweet2)

        category1 = tweet1['category']
        category2 = tweet2['category']

        if category1 not in category_list1:
            category_list1[category1] = 1
        else:
            category_list1[category1] += 1

        if category2 not in category_list2:
            category_list2[category2] = 1
        else:
            category_list2[category2] += 1

        if int(category1) != int(category2):
            print("tweet: ", tweet1["text"])
            print("file 1: category: ", category1)
            print("file 2: category: ", category2)
            mismatch += 1
        else:
            if category1 not in match_class:
                match_class[int(category1)] = 1
            else:
                match_class[int(category1)] += 1

    print("file 1 summary:")
    for word in category_list1:
        print("%s: %s" %(word, category_list1[word]))
    inFile1.close()

    print("\nfile 2 summary:")
    for word in category_list2:
        print("%s: %s" %(word, category_list2[word]))
    
    print("\nmatch list:")
    for word in match_class:
        print("%s: %s" %(word, match_class[word]))

    print("\nmismatch total:", mismatch)

    print("%s lines read" %(count))

 # ---------------------- #
if __name__ == "__main__":
    main()
