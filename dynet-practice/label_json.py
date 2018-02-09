from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

# ----- labeler function ----- #
def labeler_json():
    filename = sys.argv[2]
    inFile = open("%s" %(filename), "r")
    filename += "_labeled"
    outFile = open("%s" %(filename), "w")
    count = 0

    for line in inFile:
        tweet = json.loads(line.strip())
        print(tweet['text'].encode(encoding="utf-8"))
    	text_label = raw_input("Label: ")
    	line[label] = text_label
        count += 1
        outFile.write(line)

    inFile.close()
    outFile.close()
    print("tweet text saved in file: %s" %(filename))
    print("%s entries read" %(count))

def labeler_text():
    filename = sys.argv[2]
    inFile = open("%s" %(filename), "r")
    filename += "_labeled"
    outFile = open("%s" %(filename), "w")
    count = 0

    for line in inFile:
        count += 1
        tweet = json.loads(line.strip())
        outFile.write(tweet['text'].encode(encoding="utf-8"))
        outFile.write('\n')

    inFile.close()
    outFile.close()
    print("tweet text saved in file: %s" %(filename))
    print("%s entries read" %(count))

# ----- main ----- #
def main():
	if (int(sys.argv[1]) == 1):
		labeler_json()
	else:
		labeler_text()

# ---------------------- #
if __name__ == "__main__":
    main()
