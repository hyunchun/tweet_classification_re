from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

# ----- Extracting json from tsv file ----- #
# Name: Hyun A Chung
# filename: tsv_to_json.py
# Descripton: given tsv file and json column number, extract json and text from the json
# Output:
#   system output: number of entries read and the saved file anme
#   file output: 2 files
#       1. file with tweet json
#       2. file with tweet text only

# ----- extractor function ----- #
def extractor():
    filename = sys.argv[1]
    column_skip = int(sys.argv[2]) - 1

    inFile = open("%s" %(filename), "r")
    filename += "_version_json"
    outFile = open("%s" %(filename), "w")

    for line in inFile:
        column_count = column_skip

        for word in line:
            if (word.isspace() and (column_count != 0)):
                column_count -= 1
            elif (column_count == 0):
                outFile.write(word)

    inFile.close()
    outFile.close()

    print("json file saved in file: %s" %(filename))
    return filename

# ----- convertor function ----- #
def convertor(filename):
    inFile = open("%s" %(filename), "r")
    filename += "_text"
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
    convertor(extractor())

# ---------------------- #
if __name__ == "__main__":
    main()
