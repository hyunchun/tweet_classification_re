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
    outFile = open("%s" %(train_filename+".converted"), "w")
    count = 0
    
    for line in inFile:
        count += 1
        tweet = json.dumps(line)
        tweet = json.loads(tweet)
        tweet = json.loads(tweet)

        category = tweet['category']
        if category == "conversational":
            tweet['category'] = 1
        elif category == "status":
            tweet['category'] = 2
        elif category == "pass-along":
            tweet['category'] = 3
        elif category == "environmental":
            tweet['category'] = 4
        elif category == "politics":
            tweet['category'] = 5
        elif category == "sports":
            tweet['category'] = 6
        elif category == "technology":
            tweet['category'] = 7
        elif category == "media":
            tweet['category'] = 8
        elif category == "phatic":
            tweet['category'] = 9

        text = json.dumps(tweet)
        outFile.write(text)
        outFile.write("\n")

    inFile.close()
    outFile.close()
    print("%s lines read" %(count))

 # ---------------------- #
if __name__ == "__main__":
    main()
