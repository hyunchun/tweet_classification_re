from __future__ import print_function
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import string
import sys

def main():
    filename = sys.argv[1]
    inFile = open("%s" %(filename), "r")

    category_list = []
    count = 0
    while(count <= 1800):
        count += 100
        inFile_count = 0
        outFile = open("%s" %(filename + str(count)), "w")
        for line in inFile:
            outFile.write(line)
            inFile_count += 1
            if inFile_count == 100:
                break


    inFile.close()
    outFile.close()
 # ---------------------- #
if __name__ == "__main__":
    main()
